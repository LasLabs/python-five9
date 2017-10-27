# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import mock
import properties
import unittest

from ..models.base_model import BaseModel


class TestModel(BaseModel):
    id = properties.Integer('ID')
    not_a_field = True


class TestBaseModel(unittest.TestCase):

    def setUp(self):
        super(TestBaseModel, self).setUp()
        self.called_with = None
        self.id = 1234

    def new_record(self):
        return TestModel(
            id=self.id,
        )

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

    def test_update(self):
        """It should set the attributes to the provided values."""
        data = {'test1': 12345, 'test2': 54321}
        record = self.new_record()
        record.update(data)
        for key, value in data.items():
            self.assertEqual(getattr(record, key), value)

    def test_get_non_empty_vals(self):
        """It should return the dict without NoneTypes."""
        expect = {
            'good_int': 1234,
            'good_false': False,
            'good_true': True,
            'bad': None,
        }
        res = BaseModel.get_non_empty_vals(expect)
        del expect['bad']
        self.assertDictEqual(res, expect)

    def test_dict_lookup_exist(self):
        """It should return the attribute value when it exists."""
        self.assertEqual(
            self.new_record()['id'], self.id,
        )

    def test_dict_lookup_no_exist(self):
        """It should raise a KeyError when the attribute isn't a field."""
        with self.assertRaises(KeyError):
            self.new_record()['not_a_field']

    def test_dict_set_exist(self):
        """It should set the attribute via the items."""
        expect = 4321
        record = self.new_record()
        record['id'] = expect
        self.assertEqual(record.id, expect)

    def test_dict_set_no_exist(self):
        """It should raise a KeyError and not change the non-field."""
        record = self.new_record()
        with self.assertRaises(KeyError):
            record['not_a_field'] = False
        self.assertTrue(record.not_a_field)

    def test_get_exist(self):
        """It should return the attribute if it exists."""
        self.assertEqual(
            self.new_record().get('id'), self.id,
        )

    def test_get_no_exist(self):
        """It should return the default if the attribute doesn't exist."""
        expect = 'Test'
        self.assertEqual(
            self.new_record().get('not_a_field', expect), expect,
        )
