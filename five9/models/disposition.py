# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .base_model import BaseModel
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
    type = properties.StringChoice(
        'Disposition type.',
        choices=['FinalDisp',
                 'FinalApplyToCampaigns',
                 'AddActiveNumber',
                 'AddAndFinalize',
                 'AddAllNumbers',
                 'DoNotDial',
                 'RedialNumber',
                 ],
        descriptions={
            'FinalDisp':
                'Any contact number of the contact is not dialed again by '
                'the current campaign.',
            'FinalApplyToCampaigns':
                'Contact is not dialed again by any campaign that contains '
                'the disposition.',
            'AddActiveNumber':
                'Adds the number dialed to the DNC list.',
            'AddAndFinalize':
                'Adds the call results to the campaign history. This record '
                'is no longer dialing in this campaign. Does not add the '
                'contact\'s other phone numbers to the DNC list.',
            'AddAllNumbers':
                'Adds all the contact\'s phone numbers to the DNC list.',
            'DoNotDial':
                'Number is not dialed in the campaign, but other numbers '
                'from the CRM record can be dialed.',
            'RedialNumber':
                'Number is dialed again when the list to dial is completed, '
                'and the dialer starts again from the beginning.',
        },
    )
    typeParameters = properties.Instance(
        'Parameters that apply to the disposition type.',
        instance_class=DispositionTypeParams,
    )

    @classmethod
    def create(cls, five9, data, refresh=False):
        """Create a record on Five9.

        Args:
            five9 (five9.Five9): The authenticated Five9 remote.
            data (dict): A data dictionary that can be fed to ``deserialize``.
            refresh (bool, optional): Set to ``True`` to get the record data
                from Five9 before returning the record.

        Returns:
            BaseModel: The newly created record. If ``refresh`` is ``True``,
                this will be fetched from Five9. Otherwise, it's the data
                record that was sent to the server.
        """
        return cls._call_and_serialize(
            five9.configuration.createDisposition, data, refresh,
        )

    @classmethod
    def search(cls, five9, filters):
        """Search for a record on the remote and return the results.

        Args:
            five9 (five9.Five9): The authenticated Five9 remote.
            filters (dict): A dictionary of search parameters, keyed by the
                name of the field to search. This should conform to the
                schema defined in :func:`five9.Five9.create_criteria`.

        Returns:
            list[BaseModel]: A list of records representing the result.
        """
        return cls._name_search(five9.configuration.getDispositions, filters)

    def delete(self, five9):
        """Delete the record from the remote.

        Args:
            five9 (five9.Five9): The authenticated Five9 remote.
        """
        five9.configuration.removeDisposition(self.name)

    def write(self, five9):
        """Update the record on the remote.

        Args:
            five9 (five9.Five9): The authenticated Five9 remote.
        """
        five9.configuration.modifyDisposition(self.serialize())
