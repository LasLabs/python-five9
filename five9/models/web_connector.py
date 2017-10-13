# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .base_model import BaseModel
from .disposition import Disposition
from .key_value_pair import KeyValuePair


class WebConnector(BaseModel):
    """Contains the configuration details of a web connector."""

    addWorksheet = properties.Bool(
        'Applies only to POST requests. Whether to pass worksheet '
        'answers as parameters.',
    )
    agentApplication = properties.StringChoice(
        'If ``executeInBrowser==True``, this parameter specifies whether '
        'to open the URL in an external or an embedded browser.',
        default='EmbeddedBrowser',
        required=True,
        choices=['EmbeddedBrowser', 'ExternalBrowser'],
        descriptions={
            'EmbeddedBrowser': 'Embedded browser window.',
            'ExternalBrowser': 'External browser window.',
        },
    )
    clearTriggerDispositions = properties.Bool(
        'When modifying an existing connector, whether to clear the existing '
        'triggers.'
    )
    constants = properties.List(
        'List of parameters passed with constant values.',
        prop=KeyValuePair,
    )
    ctiWebServices = properties.StringChoice(
        'In the Internet Explorer toolbar, whether to open the HTTP request '
        'in the current or a new browser window.',
        default='CurrentBrowserWindow',
        required=True,
        choices=['CurrentBrowserWindow', 'NewBrowserWindow'],
        descriptions={
            'CurrentBrowserWindow': 'Current browser window.',
            'NewBrowserWindow': 'New browser window.',
        },
    )
    description = properties.String(
        'Purpose of the connector.',
        required=True,
    )
    executeInBrowser = properties.Bool(
        'When enabling the agent to view or enter data, whether to open '
        'the URL in an embedded or external browser window.',
        required=True,
    )
    name = properties.String(
        'Name of the connector',
        required=True,
    )
    postConstants = properties.List(
        'When using the POST method, constant parameters to pass in the URL.',
        prop=KeyValuePair,
    )
    postMethod = properties.Bool(
        'Whether the HTTP request type is POST.',
    )
    postVariables = properties.List(
        'When using the POST method, variable parameters to pass in the URL.',
        prop=KeyValuePair,
    )
    startPageText = properties.String(
        'When using the POST method, enables the administrator to enter text '
        'to be displayed in the browser (or agent Browser tab) while waiting '
        'for the completion of the connector.',
    )
    trigger = properties.StringChoice(
        'Available trigger during a call when the request is sent.',
        required=True,
        choices=['OnCallAccepted',
                 'OnCallDisconnected',
                 'ManuallyStarted',
                 'ManuallyStartedAllowDuringPreviews',
                 'OnPreview',
                 'OnContactSelection',
                 'OnWarmTransferInitiation',
                 'OnCallDispositioned',
                 'OnChatArrival',
                 'OnChatTransfer',
                 'OnChatTermination',
                 'OnChatClose',
                 'OnEmailArrival',
                 'OnEmailTransfer',
                 'OnEmailClose',
                 ],
        descriptions={
            'OnCallAccepted': 'Triggered when the call is accepted.',
            'OnCallDisconnected': 'Triggered when the call is disconnected.',
            'ManuallyStarted': 'Connector is started manually.',
            'ManuallyStartedAllowDuringPreviews': 'Connector is started '
                                                  'manually during call '
                                                  'preview.',
            'OnPreview': 'Triggered when the call is previewed.',
            'OnContactSelection': 'Triggered when a contact is selected.',
            'OnWarmTransferInitiation': 'Triggered when a warm transfer is '
                                        'initiated.',
            'OnCallDispositioned': 'Triggered when a disposition is '
                                   'selected.',
            'OnChatArrival': 'Triggered when a chat message is delivered to '
                             'an agent.',
            'OnChatTransfer': 'Triggered when a chat session is transferred.',
            'OnChatTermination': 'Triggered when the customer or the agent '
                                 'closed the session, but the agent has not '
                                 'yet set the disposition.',
            'OnChatClose': 'Triggered when the disposition is set.',
            'OnEmailArrival': 'Triggered when an email message is delivered '
                              'to the agent.',
            'OnEmailTransfer': 'Triggered when an email message is '
                               'transferred.',
            'OnEmailClose': 'Triggered when the disposition is set.',
        }
    )
    triggerDispositions = properties.List(
        'When the trigger is OnCallDispositioned, specifies the trigger '
        'dispositions.',
        prop=Disposition,
    )
    url = properties.String(
        'URI of the external web site.',
    )
    variables = properties.List(
        'When using the POST method, connectors can include worksheet data '
        'as parameter values. The variable placeholder values are surrounded '
        'by @ signs. For example, the parameter ANI has the value @Call.ANI@',
        prop=KeyValuePair,
    )

    @classmethod
    def create(cls, five9, data, refresh=False):
        return cls._call_and_serialize(
            five9.configuration.createWebConnector, data, refresh,
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
        return cls._name_search(five9.configuration.getWebConnectors, filters)

    def delete(self, five9):
        """Delete the record from the remote.

        Args:
            five9 (five9.Five9): The authenticated Five9 remote.
        """
        five9.configuration.deleteWebConnector(self.name)

    def write(self, five9):
        """Update the record on the remote.

        Args:
            five9 (five9.Five9): The authenticated Five9 remote.
        """
        five9.configuration.modifyWebConnector(self.serialize())
