# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties


class BaseModel(properties.HasProperties):
    """All models should be inherited from this.

    Currently it does nothing other than provide a common inheritance point
    within this library.
    """
