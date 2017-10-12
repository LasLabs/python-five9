# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import unittest

from ..models.web_connector import WebConnector

from .common_crud import CommonCrud


class TestWebConnector(CommonCrud, unittest.TestCase):

    Model = WebConnector

    def setUp(self):
        super(TestWebConnector, self).setUp()
        self.data['trigger'] = 'OnCallAccepted'
