from typing import Iterable, Type

from tabpipe.data_types import DataType


class DuplicateFeature(Exception):
    """Raised when a feature with the same name already exists in the dataset."""

    pass


class DuplicateTransformation(Exception):
    """Raised when a transformation with the same name already exists in the dataset."""

    pass


class UnsupportedDataframeType(Exception):
    """Raised when an unsupported dataframe type is provided."""

    pass


class NotFittedError(Exception):
    """Raised when a data transformation or pipeline is used before being fitted.

    Args:
        instance: The instance that hasn't been fitted.
    """

    def __init__(self, instance: object):
        """Initialize the NotFittedError.

        Args:
            instance: The instance that hasn't been fitted.
        """
        super().__init__(
            f"Instance of class '{instance.__class__.__name__}' hasn't been fitted yet."
        )


class MissingColumnError(ValueError):
    """Raised when a column is missing from the dataset."""

    def __init__(self, column: str, columns: Iterable[str]):
        """Initialize the MissingColumn.

        Args:
            column: The column that is missing.
            columns: The columns that are present.

        """
        super().__init__(
            f"Column '{column}' not found in dataset. Columns found: {columns}"
        )


class CastError(Exception):
    """Raised when a column cannot be cast to the desired data type.

    Args:
        column: The column that could not be cast.
        data_types: The data types that were tried.
    """

    def __init__(self, column: str, data_types: Iterable[Type[DataType]]):
        """Initialize the CastError."""
        super().__init__(
            f"Could not cast column '{column}' to any of the compatible data types: {data_types}"
        )


class DoesNotImplementInterface(Exception):
    """Raised when a class does not implement a required interface.

    Args:
        cls: The class that does not implement the interface.
        interface: The interface that is not implemented.
    """

    def __init__(self, cls: type, interface: type):
        """Initialize the DoesNotImplementInterface."""
        super().__init__(
            f"Class '{cls.__name__}' does not implement interface '{interface.__name__}'."
        )
