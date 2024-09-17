import logging
from typing import Iterable, Type

import snowflake.snowpark as snow
from typing_extensions import Self

from tabpipe.data_types import DataType
from tabpipe.dataframe.dataframe import DataFrame
from tabpipe.exceptions import MissingColumnError


class SnowparkDataFrame(DataFrame):
    """Snowpark dataframe wrapper."""

    @classmethod
    def dataframe_type(cls) -> Type:
        """The type of the dataframe."""
        return snow.DataFrame

    def filter_columns(self, columns: Iterable[str]) -> Self:
        """Filter the columns of the dataframe.

        Args:
            columns: The columns to keep.

        Returns:
            The dataframe with the filtered columns.
        """
        self.dataframe = self.dataframe.select([double_quote(c) for c in columns])
        return self

    def check_columns(self, columns: Iterable[str]) -> None:
        """Check if the columns are present in the dataframe.

        Args:
            columns: The columns to check.

        Raises:
            MissingColumnError: If a column is missing.
        """
        for column in columns:
            if double_quote(column) not in self.dataframe.columns:
                raise MissingColumnError(column, self.dataframe.columns)

    def round_column(self, column: str, precision: int) -> Self:
        """Round a column to a specific precision.

        Args:
            column: The column to round.
            precision: The number of decimal places to round to.

        Returns:
            The dataframe with the rounded column.
        """
        self.dataframe = self.dataframe.with_column(
            double_quote(column),
            snow.functions.round(self.dataframe[double_quote(column)], precision),
        )
        return self

    def cast_column(self, column: str, data_type: Type[DataType]) -> Self:
        """Cast a column to a specific data type.

        Args:
            column: The column to cast.
            data_type: The data type to cast to.

        Returns:
            The dataframe with the cast column.
        """
        self.dataframe = self.dataframe.with_column(
            double_quote(column),
            self.dataframe[double_quote(column)].cast(data_type.snowpark_type),
        )
        return self

    def sort_columns(self) -> Self:
        """Sort the columns of the dataframe in alphabetical order.

        Returns:
            The dataframe with the sorted columns.
        """
        sorted_strings = {un_double_quote(c).lower(): c for c in self.dataframe.columns}
        self.dataframe = self.dataframe.select(
            [sorted_strings[k] for k in sorted(sorted_strings)]
        )
        return self


def double_quote(name: str) -> str:
    """Wrap a name with double quotes. Useful for case sensitivity in Snowpark.

    Args:
        name: The name to format.

    Returns:
        The formatted name.

    Examples:
        >>> double_quote("age")
        '"age"'
    """
    # See if the name already contains double quotes
    double_quotes_idx = set([i for i, c in enumerate(name) if c == '"'])

    if len(double_quotes_idx) == 0:
        return f'"{name}"'
    elif double_quotes_idx == {0, len(name) - 1}:
        logging.debug(f"Name '{name}' already contains double quotes")
        return name
    else:
        raise ValueError(f"Name '{name}' makes an invalid use of double quotes")


def un_double_quote(name: str) -> str:
    """Remove double quotes from a name, usually used for case sensitivity in Snowpark.

    Args:
        name: The name to format.

    Returns:
        The formatted name.

    Examples:
        >>> un_double_quote('"age"')
        'age'
    """
    return name.strip('"')
