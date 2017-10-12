# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .base_model import BaseModel


class Timer(BaseModel):

    days = properties.Integer(
        'Number of days.'
    )
    hours = properties.Integer(
        'Number of hours.',
    )
    minutes = properties.Integer(
        'Number of minutes.',
    )
    seconds = properties.Integer(
        'Number of seconds.',
    )
