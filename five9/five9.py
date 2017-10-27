# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import requests
import zeep

from collections import OrderedDict

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote

from .environment import Environment


class Five9(object):

    WSDL_CONFIGURATION = 'https://api.five9.com/wsadmin/v9_5/' \
                         'AdminWebService?wsdl&user=%s'
    WSDL_SUPERVISOR = 'https://api.five9.com/wssupervisor/v9_5/' \
                      'SupervisorWebService?wsdl&user=%s'

    # These attributes are used to create the supervisor session.
    force_logout_session = True
    rolling_period = 'Minutes30'
    statistics_range = 'CurrentWeek'
    shift_start_hour = 8
    time_zone_offset = -7

    # API Objects
    _api_configuration = None
    _api_supervisor = None
    _api_supervisor_session = None

    @property
    def configuration(self):
        """Return an authenticated connection for use, open new if required.

        Returns:
            AdminWebService: New or existing session with the Five9 Admin Web
            Services API.
        """
        return self._cached_client('configuration')

    @property
    def supervisor(self):
        """Return an authenticated connection for use, open new if required.

        Returns:
            SupervisorWebService: New or existing session with the Five9
            Statistics API.
        """
        supervisor = self._cached_client('supervisor')
        if not self._api_supervisor_session:
            self._api_supervisor_session = self.__create_supervisor_session(
                supervisor,
            )
        return supervisor

    def __init__(self, username, password):
        self.username = username
        self.auth = requests.auth.HTTPBasicAuth(username, password)
        self.env = Environment(self)

    @staticmethod
    def create_mapping(record, keys):
        """Create a field mapping for use in API updates and creates.

        Args:
            record (BaseModel): Record that should be mapped.
            keys (list[str]): Fields that should be mapped as keys.

        Returns:
            dict: Dictionary with keys:

                * ``field_mappings``: Field mappings as required by API.
                * ``data``: Ordered data dictionary for input record.
        """

        ordered = OrderedDict()
        field_mappings = []

        for key, value in record.items():
            ordered[key] = value
            field_mappings.append({
                'columnNumber': len(ordered),  # Five9 is not zero indexed.
                'fieldName': key,
                'key': key in keys,
            })

        return {
            'field_mappings': field_mappings,
            'data': ordered,
            'fields': list(ordered.values()),
        }

    @staticmethod
    def parse_response(fields, records):
        """Parse an API response into usable objects.

        Args:
            fields (list[str]): List of strings indicating the fields that
                are represented in the records, in the order presented in
                the records.::

                [
                    'number1',
                    'number2',
                    'number3',
                    'first_name',
                    'last_name',
                    'company',
                    'street',
                    'city',
                    'state',
                    'zip',
                ]

            records (list[dict]): A really crappy data structure representing
                records as returned by Five9::

                    [
                        {
                            'values': {
                                'data': [
                                    '8881234567',
                                    None,
                                    None,
                                    'Dave',
                                    'Lasley',
                                    'LasLabs Inc',
                                    None,
                                    'Las Vegas',
                                    'NV',
                                    '89123',
                                ]
                            }
                        }
                    ]

        Returns:
            list[dict]: List of parsed records.
        """
        data = [i['values']['data'] for i in records]
        return [
            {fields[idx]: row for idx, row in enumerate(d)}
            for d in data
        ]

    @classmethod
    def create_criteria(cls, query):
        """Return a criteria from a dictionary containing a query.

        Query should be a dictionary, keyed by field name. If the value is
        a list, it will be divided into multiple criteria as required.
        """
        criteria = []
        for name, value in query.items():
            if isinstance(value, list):
                for inner_value in value:
                    criteria += cls.create_criteria({name: inner_value})
            else:
                criteria.append({
                    'criteria': {
                        'field': name,
                        'value': value,
                    },
                })
        return criteria or None

    def _get_authenticated_client(self, wsdl):
        """Return an authenticated SOAP client.

        Returns:
            zeep.Client: Authenticated API client.
        """
        return zeep.Client(
            wsdl % quote(self.username),
            transport=zeep.Transport(
                session=self._get_authenticated_session(),
            ),
        )

    def _get_authenticated_session(self):
        """Return an authenticated requests session.

        Returns:
            requests.Session: Authenticated session for use.
        """
        session = requests.Session()
        session.auth = self.auth
        return session

    def _cached_client(self, client_type):
        attribute = '_api_%s' % client_type
        if not getattr(self, attribute, None):
            wsdl = getattr(self, 'WSDL_%s' % client_type.upper())
            client = self._get_authenticated_client(wsdl)
            setattr(self, attribute, client)
        return getattr(self, attribute).service

    def __create_supervisor_session(self, supervisor):
        """Create a new session on the supervisor service.

        This is required in order to use most methods for the supervisor,
        so it is called implicitly when generating a supervisor session.
        """
        session_params = {
            'forceLogoutSession': self.force_logout_session,
            'rollingPeriod': self.rolling_period,
            'statisticsRange': self.statistics_range,
            'shiftStart': self.__to_milliseconds(
                self.shift_start_hour,
            ),
            'timeZone': self.__to_milliseconds(
                self.time_zone_offset,
            ),
        }
        supervisor.setSessionParameters(session_params)
        return session_params

    @staticmethod
    def __to_milliseconds(hour):
        return hour * 60 * 60 * 1000
