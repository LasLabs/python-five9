# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .base_model import BaseModel
from .disposition_type import DispositionType
from .disposition_type_params import DispositionTypeParams


class Disposition(BaseModel):

    agentMustCompleteWorksheet = properties.Bool(
        'Whether the agent needs to complete a worksheet before selecting '
        'a disposition.',
    )
    agentMustConfirm = properties.Bool(
        'Whether the agent is prompted to confirm the selection of the '
        'disposition.',
    )
    description = properties.String(
        'Description of the disposition.',
    )
    name = properties.String(
        'Name of the disposition.',
        required=True,
    )
    resetAttemptsCounter = properties.Bool(
        'Whether assigning the disposition resets the number of dialing '
        'attempts for this contact.',
    )
    sendEmailNotification = properties.Bool(
        'Whether call details are sent as an email notification when the '
        'disposition is used by an agent.',
    )
    sendIMNotification = properties.Bool(
        'Whether call details are sent as an instant message in the Five9 '
        'system when the disposition is used by an agent.',
    )
    trackAsFirstCallResolution = properties.Bool(
        'Whether the call is included in the first call resolution '
        'statistics (customer\'s needs addressed in the first call). Used '
        'primarily for inbound campaigns.',
    )
    type = properties.Instance(
        'Disposition type.',
        instance_class=DispositionType,
    )
    typeParameters = properties.Instance(
        'Parameters that apply to the disposition type.',
        instance_class=DispositionTypeParams,
    )
