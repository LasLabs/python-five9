# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import unittest

from ..five9 import Five9


class Common(unittest.TestCase):

    def setUp(self):
        super(Common, self).setUp()
        self.user = 'username@something.com'
        self.password = 'password'
        self.five9 = Five9(self.user, self.password)
