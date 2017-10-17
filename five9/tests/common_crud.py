# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import mock

from ..models.base_model import BaseModel


class CommonCrud(object):

    Model = BaseModel
    five9_api = 'configuration'

    def setUp(self):
        super(CommonCrud, self).setUp()
        self.data = {
            'description': 'Test',
            self.Model.__uid_field__: 'Test',
        }
        self.five9 = mock.MagicMock()
        self.model_name = self.Model.__name__
        self.method_names = {
            'create': 'create%(model_name)s',
            'write': 'modify%(model_name)s',
            'search': 'get%(model_name)ss',
            'delete': 'delete%(model_name)s',
        }

    def _get_method(self, method_type):
        method_name = self.method_names[method_type] % {
            'model_name': self.model_name,
        }
        api = getattr(self.five9, self.five9_api)
        return getattr(api, method_name)

    def test_create(self):
        """It should use the proper method and args on the API with."""
        self.Model.create(self.five9, self.data)
        self._get_method('create').assert_called_once_with(self.data)

    def test_search(self):
        """It should search the remote for the name."""
        self.Model.search(self.five9, self.data)
        self._get_method('search').assert_called_once_with(
            self.data[self.Model.__uid_field__],
        )

    def test_search_multiple(self):
        """It should search the remote for the conjoined names."""
        self.data['name'] = ['Test1', 'Test2']
        self.Model.search(self.five9, self.data)
        self._get_method('search').assert_called_once_with(
            r'(Test1|Test2)',
        )

    def test_search_return(self):
        """It should return a list of the result objects."""
        self._get_method('search').return_value = [
            self.data, self.data,
        ]
        results = self.Model.search(self.five9, self.data)
        self.assertEqual(len(results), 2)
        expect = self.Model(**self.data).serialize()
        for result in results:
            self.assertIsInstance(result, self.Model)
            self.assertDictEqual(result.serialize(), expect)

    def test_delete(self):
        """It should call the delete method and args on the API."""
        self.Model(**self.data).delete(self.five9)
        self._get_method('delete').assert_called_once_with(
            self.data[self.Model.__uid_field__],
        )

    def test_write(self):
        """It should call the write method on the API."""
        self.Model(**self.data).write(self.five9)
        self._get_method('write').assert_called_once_with(
            self.Model(**self.data).serialize(),
        )
