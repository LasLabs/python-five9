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

    _api_configuration = None
    _api_supervisor = None

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
        return self._cached_client('supervisor')

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
