# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties


class KeyValuePair(properties.HasProperties):

    key = properties.String(
        'Name used to identify the pair.',
        required=True,
    )
    value = properties.String(
        'Value that corresponds to the name.',
        required=True,
    )

    def __init__(self, key, value, **kwargs):
        """Allow for positional key, val pairs."""
        super(KeyValuePair, self).__init__(
            key=key, value=value, **kwargs
        )
