# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import unittest

from ..models.disposition import Disposition

from .common_crud import CommonCrud


class TestDisposition(CommonCrud, unittest.TestCase):

    Model = Disposition

    def setUp(self):
        super(TestDisposition, self).setUp()
        self.method_names['delete'] = 'remove%(model_name)s'
