# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from . import BaseModel


class Contact(BaseModel):
    """This represents all Contact operations."""

    first_name = properties.String(
        'First name',
    )
    last_name = properties.String(
        'Last name',
    )
    company = properties.String(
        'Company',
    )
    street = properties.String(
        'Street Address',
    )
    city = properties.String(
        'City',
    )
    state = properties.String(
        'State',
    )
    zip = properties.String(
        'Zip',
    )
    number1 = properties.String(
        'First phone number',
    )
    number1 = properties.String(
        'Second phone number',
    )
    number1 = properties.String(
        'Third phone number',
    )
