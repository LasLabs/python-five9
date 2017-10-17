# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .base_model import BaseModel
from .timer import Timer


class DispositionTypeParams(BaseModel):

    allowChangeTimer = properties.Bool(
        'Whether the agent can change the redial timer for this disposition.',
    )
    attempts = properties.Integer(
        'Number of redial attempts.',
    )
    timer = properties.Instance(
        'Redial timer.',
        instance_class=Timer,
    )
    useTimer = properties.Bool(
        'Whether this disposition uses a redial timer.',
    )
