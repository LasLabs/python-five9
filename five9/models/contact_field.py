# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from zeep.client import ServiceProxy

from . import BaseModel


class ContactField(BaseModel):
    """This represents all Contact Field operations."""

    displayAs = properties.StringChoice(
        'Display options for the data in the Agent desktop',
        choices=['Short', 'Long', 'Invisible'],
        descriptions={
            'Short': 'Half line.',
            'Long': 'Full line.',
            'Invisible': 'Not represented.',
        },
    )
    mapTo = properties.StringChoice(
        'Map of the system information inot the field. The field is '
        'updated when a disposition is set.',
        choices=['None',
                 'LastAgent',
                 'LastDisposition',
                 'LastSystemDisposition',
                 'LastAgentDisposition',
                 'LastDispositionDateTime',
                 'LastSystemDispositionDateTime',
                 'LastAgentDispositionDateTime',
                 'LastAttemptedNumber',
                 'LastAttemptedNumberN1N2N3',
                 'LastCampaign',
                 'AttemptsForLastCampaign',
                 'LastList',
                 'CreatedDateTime',
                 'LastModifiedDateTime',
                 ],
        descriptions={
            'None': 'No mapping.',
            'LastAgent': 'Name of last logged-in agent.',
            'LastDisposition': 'Name of last disposition assigned to a call.',
            'LastSystemDisposition': 'Name of last system disposition '
                                     'assigned to a call.',
            'LastAgentDisposition': 'Name of last disposition assigned by an '
                                    'agent to a call.',
            'LastDispositionDateTime': 'Date and time of last disposition '
                                       'assigned to a call',
            'LastSystemDispositionDateTime': 'Date and time of last system '
                                             'disposition assigned to a '
                                             'call.',
            'LastAgentDispositionDateTime': 'Date and time of last '
                                            'disposition assigned by an '
                                            'agent to a call.',
            'LastAttemptedNumber': 'Last number attempted by the dialer or '
                                   'by an agent.',
            'LastAttemptedNumberN1N2N3': 'Index of the last dialed phone '
                                         'number in the record: number1, '
                                         'number2 or number3.',
            'LastCampaign': 'Name of the last campaign that dialed the '
                            'record.',
            'AttemptsForLastCampaign': 'Dialing attempts for last campaign.',
            'LastList': 'Name of last list used.',
            'CreatedDateTime': 'Date and time of record creation in the '
                               'contact database.',
            'LastModifiedDateTime': 'Date and time of record modification in '
                                    'the contact database.',
        },
    )
    name = properties.String(
        'Name of the contact field.',
    )
    restrictions = properties.basic.DynamicProperty(
        'Restrictions imposed on the data that can be stored in this field. '
        'Not currently mapped.',
    )
    system = properties.Bool(
        'Whether this field is set by the system or an agent. \n\n'
        '• ``True``: Field set by system. \n'
        '• ``False``: Field set by agent. \n'
    )
    type = properties.StringChoice(
        'The type of data stored in this field.',
        choices=['STRING',
                 'NUMBER',
                 'DATE',
                 'TIME',
                 'DATE_TIME',
                 'CURRENCY',
                 'BOOLEAN',
                 'PERCENT',
                 'EMAIL',
                 'URL',
                 'PHONE',
                 'TIME_PERIOD',
                 ],
    )

    def create(self):
        return self.five9.configuration.createContactField(
            field=self.to_api(),
        )

    def delete(self):
        return self.five9.configuration.deleteContactField(
            fieldName=self.name,
        )

    @classmethod
    @BaseModel.api
    def get(cls, name_pattern):
        response = cls.five9.configuration.getContactFields(
            namePattern=name_pattern,
        )
        return [cls(**response)]

    def update(self):
        return self.five9.configuration.modifyContactField(
            field=self.to_api()
        )
