# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import unittest

from ..models.key_value_pair import KeyValuePair


class TestKeyValuePair(unittest.TestCase):

    def test_init_positional(self):
        """It should allow positional key, value pairs."""
        res = KeyValuePair('key', 'value')
        self.assertEqual(res.key, 'key')
        self.assertEqual(res.value, 'value')
