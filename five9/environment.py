# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from .exceptions import ValidationError


class Api(object):
    """This is a set of decorators for model validators."""

    @staticmethod
    def model(method):
        """Use this to decorate methods that expect a model."""
        def wrapper(self, *args, **kwargs):
            if self.__model__ is None:
                raise ValidationError(
                    'You cannot perform CRUD operations without selecting a '
                    'model first.',
                )
            return method(self, *args, **kwargs)
        return wrapper

    @staticmethod
    def recordset(method):
        """Use this to decorate methods that expect a record set."""
        def wrapper(self, *args, **kwargs):
            if self.__records__ is None:
                raise ValidationError(
                    'There are no records in the set.',
                )
            return method(self, *args, **kwargs)
        return Api.model(wrapper)


class Environment(object):
    """Represents a container for models with a back-reference to Five9.
    """

    # The authenticated ``five9.Five9`` object.
    __five9__ = None
    # A dictionary of models, keyed by class name.
    __models__ = None
    # The currently selected model.
    __model__ = None
    # A list of records represented by this environment.
    __records__ = None
    # The current record represented by this environment.
    __record__ = None

    @classmethod
    def __new__(cls, *args, **kwargs):
        """Find and cache all model objects, if not already done."""
        if cls.__models__ is None:
            models = __import__('five9').models
            cls.__models__ = {
                model: getattr(models, model)
                for model in models.__all__
                if not model.startswith('_')
            }
        return object.__new__(cls)

    def __init__(self, five9, model=None, records=None):
        """Instantiate a new environment."""
        self.__five9__ = five9
        self.__model__ = model
        self.__records__ = records

    def __getattribute__(self, item):
        try:
            return super(Environment, self).__getattribute__(item)
        except AttributeError:
            return self.__class__(self.__five9__, self.__models__[item])

    @Api.recordset
    def __iter__(self):
        """Pass iteration through to the records.

        Yields:
            BaseModel: The next record in the iterator.

        Raises:
            StopIterationError: When all records have been iterated.
        """
        for record in self.__records__:
            self.__record__ = record
            yield record
        raise StopIteration()

    @Api.model
    def create(self, data, refresh=False):
        """Create the data on the remote, optionally refreshing."""
        self.__model__.create(self.__five9__, data)
        if refresh:
            return self.read(data[self.__model__.__name__])
        else:
            return self.new(data)

    @Api.model
    def new(self, data):
        """Create a new memory record, but do not create on the remote."""
        return self.__class__(
            self.__five9__,
            self.__model__,
            records=[self.__model__.deserialize(data)],
        )

    @Api.model
    def read(self, external_id):
        """Perform a lookup on the current model for the provided external ID.
        """
        return self.__model__.read(self.__five9__, external_id)

    @Api.recordset
    def write(self):
        """Write the records to the remote."""
        return self._iter_call('write')

    @Api.recordset
    def delete(self):
        """Delete the records from the remote."""
        return self._iter_call('delete')

    @Api.model
    def search(self, filters):
        """Search Five9 given a filter.

        Args:
            filters (dict): A dictionary of search strings, keyed by the name
                of the field to search.

        Returns:
            Environment: An environment representing the recordset.
        """
        records = self.__model__.search(self.__five9__, filters)
        return self.__class__(
            self.__five9__, self.__model__, records,
        )

    @Api.recordset
    def _iter_call(self, method_name):
        return [
            getattr(r, method_name)(self.__five9__) for r in self.__records__
        ]
