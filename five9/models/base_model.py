# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties


class BaseModel(properties.HasProperties):
    """All models should be inherited from this.

    Currently it does nothing other than provide a common inheritance point
    within this library, plus a CRUD skeleton.
    """

    # This is the attribute on Five9 that serves as the UID for Five9.
    # Typically this is ``name``.
    __uid_field__ = 'name'

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
        raise NotImplementedError()

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
        raise NotImplementedError()

    @classmethod
    def read(cls, five9, external_id):
        """Return a record singleton for the ID.

        Args:
            five9 (five9.Five9): The authenticated Five9 remote.
            external_id (mixed): The identified on Five9. This should be the
                value that is in the ``__uid_field__`` field on the record.

        Returns:
            BaseModel: The record, if found. Otherwise ``None``
        """
        results = cls.search(five9, {cls.__uid_field__: external_id})
        if not results:
            return None
        return results[0]

    def delete(self, five9):
        """Delete the record from the remote.

        Args:
            five9 (five9.Five9): The authenticated Five9 remote.
        """
        raise NotImplementedError()

    def update(self, five9):
        """Update the record on the remote.

        Args:
            five9 (five9.Five9): The authenticated Five9 remote.
        """
        raise NotImplementedError()

    @classmethod
    def _call_and_serialize(cls, method, data, refresh=False):
        """Call the remote method with data, and optionally refresh.

        Args:
            method (callable): The method on the Authenticated Five9 object
                that should be called.
            data (dict): A data dictionary that will be passed as the first
                and only position argument to ``method``.
            refresh (bool, optional): Set to ``True`` to get the record data
                from Five9 before returning the record.

        Returns:
            BaseModel: The newly created record. If ``refresh`` is ``True``,
                this will be fetched from Five9. Otherwise, it's the data
                record that was sent to the server.
        """
        method(data)
        if refresh:
            return cls.read(method.__self__, data[cls.__uid_field__])
        else:
            return cls.deserialize(data)
