# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import mock
import unittest

from ..models.web_connector import WebConnector


class TestWebConnector(unittest.TestCase):

    def setUp(self):
        super(TestWebConnector, self).setUp()
        self.connector = WebConnector(
            description='Test',
            name='Test',
            trigger='OnCallAccepted',
        )

    def test_create(self):
        """It should use the proper method and args on the API with."""
        five9 = mock.MagicMock()
        self.connector.create(five9)
        five9.configuration.createWebConnector.assert_called_once_with(
            self.connector.serialize(),
        )
