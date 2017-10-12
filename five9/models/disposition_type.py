# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .base_model import BaseModel


class DispositionType(BaseModel):

    FinalDisp = properties.String(
        'Any contact number of the contact is not dialed again by '
        'the current campaign.',
    )
    FinalApplyToCampaigns = properties.String(
        'Contact is not dialed again by any campaign that contains the '
        'disposition.',
    )
    AddActiveNumber = properties.String(
        'Adds the number dialed to the DNC list.',
    )
    AddAndFinalize = properties.String(
        'Adds the call results to the campaign history. This record is no '
        'longer dialing in this campaign. Does not add the contact\'s other '
        'phone numbers to the DNC list.',
    )
    AddAllNumbers = properties.String(
        'Adds all the contact\'s phone numbers to the DNC list.',
    )
    DoNotDial = properties.String(
        'Number is not dialed in the campaign, but other numbers from the '
        'CRM record can be dialed.',
    )
    RedialNumber = properties.String(
        'Number is dialed again when the list to dial is completed, and the '
        'dialer starts again from the beginning.',
    )
