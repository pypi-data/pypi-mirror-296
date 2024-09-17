import logging
from abc import ABC, abstractmethod
from typing import Any, Iterable, Type

from typing_extensions import Self

from tabpipe.data_types import DataType
from tabpipe.exceptions import CastError, UnsupportedDataframeType


class DataFrame(ABC):
    """Dataframe interface.

    This class defines the interface for a dataframe wrapper.
    It is used to abstract some of the core functionalities of dataframes.

    The purpose of this class is not to entirely abstract data manipulation,
    since we still want to be able to delegate that part of the abstraction to the
    Transformation subclasses. Instead, this class is meant to abstract the simpler
    operations (e.g. filtering columns, validating columns, etc.) that need to be
    available to the pipelining logic.

    Perhaps in a future version of the library, we could consider actually
    abstracting the data manipulation part, which could make sense and make the
    implementation of Transformation subclasses easier and more elegant, but for now
    that is out of scope for this project.
    """

    @classmethod
    @abstractmethod
    def dataframe_type(cls) -> Type:
        """The type of the dataframe."""
        pass

    @property
    def dataframe(self) -> Any:
        """The wrapped dataframe object."""
        return self._dataframe

    @dataframe.setter
    def dataframe(self, dataframe: Any) -> None:
        """Set the wrapped dataframe object.

        Args:
            dataframe: The dataframe to wrap.
        """
        if not isinstance(dataframe, self.dataframe_type()):
            raise UnsupportedDataframeType(type(dataframe))
        self._dataframe = dataframe

    def __init__(self, dataframe: object) -> None:
        """Initialize the dataframe wrapper.

        Args:
            dataframe: The dataframe to wrap.
        """
        self.dataframe = dataframe

    @classmethod
    def from_object(cls, dataframe: object) -> Self:
        """Create a DataFrame object from one of the supported dataframe types.

        Args:
            dataframe: The dataframe object to wrap.
        """
        if isinstance(dataframe, cls):
            return dataframe

        for subclass in cls.__subclasses__():
            if isinstance(dataframe, subclass.dataframe_type()):
                return subclass(dataframe)

        raise UnsupportedDataframeType(type(dataframe))

    @abstractmethod
    def filter_columns(self, columns: Iterable[str]) -> Self:
        """Filter the columns of the dataframe.

        Args:
            columns: The columns to keep.

        Returns:
            The dataframe with the filtered columns.
        """
        pass

    @abstractmethod
    def check_columns(self, columns: Iterable[str]) -> None:
        """Check if the columns are present in the dataframe.

        Args:
            columns: The columns to check.
        """
        pass

    @abstractmethod
    def round_column(self, column: str, precision: int) -> Self:
        """Round a column to a specific precision.

        Args:
            column: The column to round.
            precision: The precision to round the column to.

        Returns:
            The rounded dataframe.
        """
        pass

    @abstractmethod
    def cast_column(self, column: str, data_type: Type[DataType]) -> Self:
        """Cast a column to a specific data type."""
        pass

    @abstractmethod
    def sort_columns(self) -> Self:
        """Sort the columns of the dataframe."""
        pass

    def format_column(self, column: str, data_type: Type[DataType]) -> Self:
        """Format a column name for a specific data type.

        Args:
            column: The column to format.
            data_type: The data type to format the column for.
        """
        df = self.dataframe
        succeeded = False
        compatible_data_types = data_type.get_compatibles()
        for compatible_type in compatible_data_types:
            try:
                df = self.cast_column(column, compatible_type)
                succeeded = True
                break
            except Exception as e:
                logging.debug(
                    f"Could not cast column '{column}' to data type '{compatible_type}': {e}"
                )

        if not succeeded:
            raise CastError(column, compatible_data_types)

        type_precision = compatible_type.get_precision()
        if type_precision is not None:
            df = self.round_column(column, type_precision)

        return df
