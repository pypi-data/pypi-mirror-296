"""
Store and analyze data on differences in parameters, given oasdiff data.
"""
from typing import Union
import json
from abc import ABCMeta, abstractmethod


def make_hashable(obj):
    """Recursively convert a dictionary or list into a hashable type."""
    if isinstance(obj, dict):
        return frozenset((key, make_hashable(value)) for key, value in obj.items())
    elif isinstance(obj, list):
        return tuple(make_hashable(item) for item in obj)
    elif isinstance(obj, set):
        return frozenset(make_hashable(item) for item in obj)
    else:
        return obj


class ParameterType(object):
    """
    Abstract type for parameter data.

    We can have sub-types for parameters that require loading from different parts of the oasdiff data.

    """
    __meta_class__ = ABCMeta

    def __init__(self):
        self.data: dict = {}
        self.parameter_type: Union[str, None] = None
        self.name: Union[str, None] = None
        self.http_method: Union[str, None] = None
        self.path: Union[str, None] = None

    def __eq__(self, other):
        return (self.data == other.data and
                self.parameter_type == other.parameter_type and
                self.name == other.name and
                self.http_method == other.http_method and
                self.path == other.path)

    def __lt__(self, other):
        """Implement the less-than operator, so we can make this class sortable in a list."""
        return (self.parameter_type, self.path, self.http_method, self.name) < (
            other.parameter_type, other.path, other.http_method, other.name)

    def __hash__(self):
        """
        Define a hash function that ensures objects with the same attribute values
        have the same hash. Use immutable data types (tuples) in the hash calculation.
        """
        return hash((
            make_hashable(self.data),  # Ensure the data is hashable
            self.parameter_type,
            self.name,
            self.http_method,
            self.path
        ))

    def __str__(self):
        return self.data

    def __repr__(self):
        return f"{self.__class__.__name__} (http_method={self.http_method}, path={self.path}, parameter_type={self.parameter_type}, name={self.name})"

    @abstractmethod
    def changed_requirement_status(self) -> bool:
        """
        Did the parameter change from required to not required, or vice versa?
        """
        raise NotImplementedError

    @abstractmethod
    def old_requirement_status(self) -> Union[bool, None]:
        """
        If the requirement status changed, return the old status.
        """
        raise NotImplementedError

    @abstractmethod
    def new_requirement_status(self) -> Union[bool, None]:
        """
        If the requirement status changed, return the new status.
        """
        raise NotImplementedError

    @abstractmethod
    def changed_default_value(self) -> bool:
        """
        Did the parameter change the default value?
        """
        raise NotImplementedError

    @abstractmethod
    def old_default_value(self) -> Union[bool, None]:
        """
        If the default value changed, return the old value.
        """
        raise NotImplementedError

    @abstractmethod
    def new_default_value(self) -> Union[bool, None]:
        """
        If the default value changed, return the new value.
        """
        raise NotImplementedError

    @abstractmethod
    def changed_variable_type(self) -> bool:
        """
        Did the parameter change the type?
        """
        raise NotImplementedError

    @abstractmethod
    def old_variable_type(self) -> Union[bool, None]:
        """
        If the type changed, return the old type.
        """
        raise NotImplementedError

    @abstractmethod
    def new_variable_type(self) -> Union[bool, None]:
        """
        If the type changed, return the new type.
        """
        raise NotImplementedError

    @abstractmethod
    def changed_schema(self) -> bool:
        """
        Did the parameter change the schema?
        """
        raise NotImplementedError

    def to_dict(self):
        """Convert the object to a dictionary for JSON serialization."""
        return {
            'data': self.data,
            'parameter_type': self.parameter_type,
            'name': self.name,
            'http_method': self.http_method,
            'path': self.path
        }


# Custom JSON encoder for serializing ModifiedParameterDataEncoder objects
class ParameterDataJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ParameterType):
            return obj.to_dict()
        # Let the base class default method handle other objects
        return super().default(obj)

