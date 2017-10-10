# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import mock
import unittest

from ..models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):

    def setUp(self):
        super(TestBaseModel, self).setUp()
        self.called_with = None

    def _test_method(self, data):
        self.called_with = data

    def test_read_none(self):
        """It should return None if no result."""
        with mock.patch.object(BaseModel, 'search') as search:
            search.return_value = []
            self.assertIsNone(BaseModel.read(None, None))

    def _call_and_serialize(self, data=None, refresh=False):
        method = self._test_method
        result = BaseModel._call_and_serialize(method, data, refresh)
        return result

    def test_read_results(self):
        """It should return the first result."""
        with mock.patch.object(BaseModel, 'search') as search:
            search.return_value = [1, 2]
            self.assertEqual(BaseModel.read(None, None), 1)

    def test_read_search(self):
        """It should perform the proper search."""
        with mock.patch.object(BaseModel, 'search') as search:
            BaseModel.read('five9', 'external_id')
            search.assert_called_once_with('five9', {'name': 'external_id'})

    def test_call_and_serialize_refresh_return(self):
        """It should return the refreshed object."""
        data = {'name': 'test'}
        with mock.patch.object(BaseModel, 'read') as read:
            result = self._call_and_serialize(data, True)
            read.assert_called_once_with(self, data['name'])
            self.assertEqual(self.called_with, data)
            self.assertEqual(result, read())

    def test_call_and_serialize_no_refresh(self):
        """It should return the deserialized data."""
        data = {'name': 'test'}
        with mock.patch.object(BaseModel, 'deserialize') as deserialize:
            result = self._call_and_serialize(data, False)
            deserialize.assert_called_once_with(data)
            self.assertEqual(self.called_with, data)
            self.assertEqual(result, deserialize())
