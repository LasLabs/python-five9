# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import mock
import unittest

from ..environment import Environment
from ..five9 import Five9
from ..models.web_connector import WebConnector


class TestEnvironment(unittest.TestCase):

    def setUp(self):
        super(TestEnvironment, self).setUp()
        self.five9 = mock.MagicMock(spec=Five9)
        self.records = [
            mock.MagicMock(spec=WebConnector),
            mock.MagicMock(spec=WebConnector),
        ]
        self.model = mock.MagicMock(spec=WebConnector)
        self.model.__name__ = 'name'
        self.env = Environment(self.five9, self.model, self.records)

    def _test_iter_method(self, method_name):
        getattr(self.env, method_name)()
        for record in self.records:
            getattr(record, method_name).assert_called_once_with(self.five9)

    def test_new_gets_models(self):
        """It should assign the ``__models__`` class attribute."""
        self.assertIsInstance(Environment.__models__, dict)
        self.assertGreater(len(Environment.__models__), 1)

    def test_init_sets_five9(self):
        """It should set the __five9__ attribute."""
        self.assertEqual(self.env.__five9__, self.five9)

    def test_init_sets_records(self):
        """It should set the __records__ attribute."""
        self.assertEqual(self.env.__records__, self.records)

    def test_init_sets_model(self):
        """It should set the __model__ attribute."""
        self.assertEqual(self.env.__model__, self.model)

    def test_getattr_pass_through_to_model(self):
        """It should return the correct model environment."""
        self.assertEqual(self.env.WebConnector.__model__, WebConnector)

    def test_iter(self):
        """It should iterate the records in the set."""
        for idx, record in enumerate(self.env):
            self.assertEqual(record, self.records[idx])
            self.assertEqual(self.env.__record__, self.records[idx])

    def test_create_creates(self):
        """It should create the record on the remote."""
        expect = {'test': 1234}
        self.env.create(expect)
        self.model.create.assert_called_once_with(self.five9, expect)

    def test_create_return_refreshed(self):
        """It should create the refreshed record when True."""
        expect = {'name': 1234}
        with mock.patch.object(self.env, 'read') as read:
            res = self.env.create(expect, True)
            read.assert_called_once_with(expect[self.model.__name__])
            self.assertEqual(res, read())

    def test_create_return_deserialized(self):
        """It should return a deserialized memory record if no refresh."""
        expect = {'test': 1234}
        res = self.env.create(expect, False)
        self.model.deserialize.assert_called_once_with(expect)
        self.assertEqual(len(res.__records__), 1)
        self.assertEqual(res.__records__[0], self.model.deserialize())

    def test_read(self):
        """It should call and return properly."""
        expect = 1234
        res = self.env.read(expect)
        self.model.read.assert_called_once_with(self.five9, expect)
        self.assertEqual(res, self.model.read())

    def test_write(self):
        """It should iterate and write the recordset."""
        self._test_iter_method('write')

    def test_delete(self):
        """It should iterate and delete the recordset."""
        self._test_iter_method('delete')

    def test_search(self):
        """It should call search on the model and return a recordset."""
        expect = {'test': 1234}
        results = self.env.search(expect)
        self.model.search.assert_called_once_with(self.five9, expect)
        self.assertEqual(results.__records__, self.model.search())
