# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import mock
import requests

from collections import OrderedDict

from .common import Common


class TestFive9(Common):

    def test_create_criteria_flat(self):
        """It should return the proper criteria for the flat inputs."""
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'number1': 1234567890,
        }
        result = self.five9.create_criteria(data)
        self.assertEqual(len(result), len(data))
        for key, value in data.items():
            criteria = {'criteria': {'field': key, 'value': value}}
            self.assertIn(criteria, result)

    def test_create_criteria_list(self):
        """It should create multiple criteria for a list."""
        data = {
            'first_name': ['Test1', 'Test2'],
        }
        result = self.five9.create_criteria({
            'first_name': ['Test1', 'Test2'],
        })
        self.assertEqual(len(result), 2)
        for name in data['first_name']:
            criteria = {'criteria': {'field': 'first_name', 'value': name}}
            self.assertIn(criteria, result)

    def test_create_mapping(self):
        """It should output the proper mapping."""
        record = OrderedDict([
            ('first_name', 'Test'),
            ('last_name', 'User'),
        ])
        result = self.five9.create_mapping(record, ['last_name'])
        expect = {
            'field_mappings': [
                {'columnNumber': 1, 'fieldName': 'first_name', 'key': False},
                {'columnNumber': 2, 'fieldName': 'last_name', 'key': True},
            ],
            'data': record,
            'fields': ['Test', 'User'],
        }
        self.assertDictEqual(result, expect)

    def test_parse_response(self):
        """It should return the proper record."""
        expect = [
            OrderedDict([('first_name', 'Test'), ('last_name', 'User')]),
            OrderedDict([('first_name', 'First'), ('last_name', 'Last')]),
        ]
        fields = ['first_name', 'last_name']
        records = [{'values': {'data': list(e.values())}} for e in expect]
        response = self.five9.parse_response(fields, records)
        for idx, row in enumerate(response):
            self.assertDictEqual(row, expect[idx])

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

    def test_supervisor_session(self):
        """It should automatically create a supervisor session."""
        response, _ = self._test_cached_client('supervisor')
        response.setSessionParameters.assert_called_once_with(
            self.five9._api_supervisor_session,
        )

    def test_supervisor_session_cached(self):
        """It should use a cached supervisor session after initial."""
        response, _ = self._test_cached_client('supervisor')
        self._test_cached_client('supervisor')
        response.setSessionParameters.assert_called_once()
