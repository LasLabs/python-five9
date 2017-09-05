# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import mock
import requests
import unittest

from ..five9 import Five9


class TestFive9(unittest.TestCase):

    def setUp(self):
        super(TestFive9, self).setUp()
        self.user = 'username@something.com'
        self.password = 'password'
        self.five9 = Five9(self.user, self.password)

    def _test_cached_client(self, client_type):
        with mock.patch.object(self.five9, '_get_authenticated_client') as mk:
            response = getattr(self.five9, client_type)
        return response, mk

    def test_init_username(self):
        """It should assign the username during init."""
        self.assertEqual(self.five9.username, self.user)

    def test_init_authentication(self):
        """It should create a BasicAuth object with proper args."""
        self.assertIsInstance(self.five9.auth, requests.auth.HTTPBasicAuth)
        self.assertEqual(self.five9.auth.username, self.user)
        self.assertEqual(self.five9.auth.password, self.password)

    @mock.patch('five9.five9.zeep')
    def test_get_authenticated_client(self, zeep):
        """It should return a zeep client."""
        wsdl = 'wsdl%s'
        response = self.five9._get_authenticated_client(wsdl)
        zeep.Client.assert_called_once_with(
            wsdl % self.user.replace('@', '%40'),
            transport=zeep.Transport(),
        )
        self.assertEqual(response, zeep.Client())

    def test_get_authenticated_session(self):
        """It should return a requests session with authentication."""
        response = self.five9._get_authenticated_session()
        self.assertIsInstance(response, requests.Session)
        self.assertEqual(response.auth, self.five9.auth)

    def test_configuration(self):
        """It should return an authenticated configuration service."""
        response, mk = self._test_cached_client('configuration')
        mk.assert_called_once_with(self.five9.WSDL_CONFIGURATION)
        self.assertEqual(response, mk().service)

    def test_supervisor(self):
        """It should return an authenticated supervisor service."""
        response, mk = self._test_cached_client('supervisor')
        mk.assert_called_once_with(self.five9.WSDL_SUPERVISOR)
        self.assertEqual(response, mk().service)
