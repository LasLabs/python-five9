# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties


class BaseModel(properties.HasProperties):
    """This is the core interface to be inherited by all models."""

    # The authenticated Five9 interface that should be used for the
    # underlying data operations. This is set using the
    five9 = None

    @staticmethod
    def api(method):
        """Use this decorator to wrap methods that interact with the API.

        These methods should always be called with an authenticated API
        interface for their first parameter. This interface will be set as
        the ``five9`` object, with the rest of the arguments being passed to
        the actual method.
        """

        def decorated_method(self, api, *args, **kwargs):
            self.five9 = api
            return method(*args, **kwargs)

        return decorated_method

    @classmethod
    def parse_response(cls, fields, records):
        """Parse an API response into usable objects.

        Args:
            fields (list[str]): List of strings indicating the fields that
                are represented in the records, in the order presented in
                the records.::

                [
                    'number1',
                    'number2',
                    'number3',
                    'first_name',
                    'last_name',
                    'company',
                    'street',
                    'city',
                    'state',
                    'zip',
                ]

            records (list[dict]): A really crappy data structure representing
                records as returned by Five9::

                    [
                        {
                            'values': {
                                'data': [
                                    '8881234567',
                                    None,
                                    None,
                                    'Dave',
                                    'Lasley',
                                    'LasLabs Inc',
                                    None,
                                    'Las Vegas',
                                    'NV',
                                    '89123',
                                ]
                            }
                        }
                    ]

        Returns:
            list[BaseModel]: List of parsed records.
        """
        data = [i['values']['data'] for i in records]
        return [
            cls(**{fields[idx]: row for idx, row in enumerate(d)})
            for d in data
        ]

    def to_api(self):
        """Return all of the properties and values in a dictionary."""
        return {
            attr: getattr(self, attr) for attr in self._props.keys(),
        }

    def __getattr__(self, item):
        """Allow for dynamic attributes, because the fields can be changed.

        Items beginning with ``_`` are excluded from  this logic.
        """
        if item.startswith('_'):
            return super(BaseModel, self).__getattr__(item)
        try:
            return super(BaseModel, self).__getattr__(item)
        except AttributeError:
            private_attr = '_%s' % item
            try:
                return super(BaseModel, self).__getattr__(private_attr)
            except AttributeError:
                new_attr = properties.basic.DynamicProperty(
                    'This is a dynamically created attribute.',
                )
                setattr(self, private_attr, new_attr)
                self._props[item] = new_attr
            return super(BaseModel, self).__getattr__(private_attr)

    # CRUD Interface
    def create(self):
        """Create the object on the API. Children should implement this."""
        raise NotImplementedError

    def delete(self):
        """Delete the object from the API. Chilren should implement this."""
        raise NotImplementedError

    @classmethod
    def get(cls, identifier):
        """Get the object from the API. Children should implement this.

        Args:
            identifier (mixed): The identifier to send as the search key.

        Returns:
            list[BaseModel]: Recordset matching identifier.
        """
        raise NotImplementedError

    @classmethod
    def search(cls, query):
        """Search for the query."""
        raise NotImplementedError

    def update(self):
        """Update the object on the API. Children should implement this."""
        raise NotImplementedError

    def upsert(self):
        """Create or Update the object on the API. Children should implement.
        """
        raise NotImplementedError
