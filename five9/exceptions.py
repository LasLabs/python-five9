# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).


class Five9Exception(Exception):
    """Base Five9 Exceptions."""


class ValidationError(Five9Exception):
    """Indicated an error validating user supplied data."""
