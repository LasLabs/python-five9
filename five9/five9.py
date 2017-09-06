# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import requests
import zeep

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote


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
