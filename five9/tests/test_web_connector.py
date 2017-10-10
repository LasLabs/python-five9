# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import mock
import unittest

from ..models.web_connector import WebConnector


class TestWebConnector(unittest.TestCase):

    def setUp(self):
        super(TestWebConnector, self).setUp()
        self.data = dict(
            description='Test',
            name='Test',
            trigger='OnCallAccepted',
        )
        self.five9 = mock.MagicMock()

    def test_create(self):
        """It should use the proper method and args on the API with."""
        WebConnector.create(self.five9, self.data)
        self.five9.configuration.createWebConnector.assert_called_once_with(
            self.data,
        )

    def test_search_assert(self):
        """It should raise AssertionError when no name in filter."""
        filter = {'test': 1234}
        with self.assertRaises(AssertionError):
            WebConnector.search(self.five9, filter)

    def test_search(self):
        """It should search the remote and return the results."""
        WebConnector.search(self.five9, self.data)
        self.five9.configuration.getWebConnectors.assert_called_once_with(
            self.data['name'],
        )

    def test_search_return(self):
        """It should return a list of the result objects."""
        self.five9.configuration.getWebConnectors.return_value = [
            self.data, self.data,
        ]
        results = WebConnector.search(self.five9, self.data)
        self.assertEqual(len(results), 2)
        expect = WebConnector(**self.data).serialize()
        for result in results:
            self.assertIsInstance(result, WebConnector)
            self.assertDictEqual(result.serialize(), expect)

    def test_delete(self):
        """It should call the delete method and args on the API."""
        WebConnector(**self.data).delete(self.five9)
        self.five9.configuration.deleteWebConnector.assert_called_once_with(
            self.data['name'],
        )

    def test_update(self):
        """It should call the update method on the API."""
        WebConnector(**self.data).update(self.five9)
        self.five9.configuration.modifyWebConnector.assert_called_once_with(
            WebConnector(**self.data).serialize(),
        )
