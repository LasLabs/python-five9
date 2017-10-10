# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import unittest

from ..environment import Api
from ..exceptions import ValidationError


class TestRecord(object):

    __model__ = None
    __records__ = None

    @Api.model
    def model(self):
        return True

    @Api.recordset
    def recordset(self):
        return True


class TestApi(unittest.TestCase):

    def setUp(self):
        super(TestApi, self).setUp()
        self.record = TestRecord()

    def test_model_bad(self):
        """It should raise ValidationError when no model."""
        with self.assertRaises(ValidationError):
            self.record.model()

    def test_recordset_bad(self):
        """It should raise ValidationError when no recordset."""
        self.record.__model__ = False
        with self.assertRaises(ValidationError):
            self.record.recordset()

    def test_recordset_model(self):
        """It should raise ValidationError when recordset but no model."""
        with self.assertRaises(ValidationError):
            self.record.__records__ = [1]
            self.record.recordset()

    def test_recordset_valid(self):
        """It should return True when valid recordset method."""
        self.record.__records__ = [1]
        self.record.__model__ = True
        self.assertTrue(self.record.recordset())

    def test_model_valid(self):
        """It should return True when valid model method."""
        self.record.__model__ = True
        self.assertTrue(self.record.model())
