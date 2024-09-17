from typing import Iterable, Type

import pandas as pd
from typing_extensions import Self

from tabpipe.data_types import DataType
from tabpipe.dataframe.dataframe import DataFrame
from tabpipe.exceptions import MissingColumnError


class PandasDataFrame(DataFrame):
    """Pandas dataframe wrapper."""

    @classmethod
    def dataframe_type(cls) -> Type:
        """The type of the dataframe."""
        return pd.DataFrame

    def filter_columns(self, columns: Iterable[str]) -> Self:
        """Filter the columns of the dataframe.

        Args:
            columns: The columns to keep.

        Returns:
            The dataframe with the filtered columns.
        """
        self.dataframe = self.dataframe[columns]
        return self

    def check_columns(self, columns: Iterable[str]) -> None:
        """Check if the columns are present in the dataframe.

        Args:
            columns: The columns to check.
        """
        for column in columns:
            if column not in self.dataframe.columns:
                raise MissingColumnError(column, self.dataframe.columns)

    def round_column(self, column: str, precision: int) -> Self:
        """Round a column to a given precision.

        Args:
            column: The column to round.
            precision: The precision to round to.

        Returns:
            The dataframe with the rounded column.
        """
        self.dataframe = self.dataframe.round({column: precision})
        return self

    def cast_column(self, column: str, data_type: Type[DataType]) -> Self:
        """Cast a column to a given data type.

        Args:
            column: The column to cast.
            data_type: The data type to cast to.

        Returns:
            The dataframe with the cast column.
        """
        self.dataframe = self.dataframe.astype({column: data_type.pandas_type})
        return self

    def sort_columns(self) -> Self:
        """Sort the columns of the dataframe.

        Returns:
            The dataframe with the sorted columns.
        """
        self.dataframe = self.dataframe.reindex(sorted(self.dataframe.columns), axis=1)
        return self
