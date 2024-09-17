from enum import Enum
from typing import Callable, Collection, Dict, Type

import pandas as pd
import snowflake.snowpark as snow

from tabpipe.data_types import DataType, IntDataType
from tabpipe.dataframe.snowpark import double_quote
from tabpipe.transformations.transformation import (
    FixedOutputTransformation,
    NoFitTransformation,
    SupportsPandas,
    SupportsSnowpark,
    Transformation,
    validate_inputs,
)
from tabpipe.units import DateTimeParts


@validate_inputs(nr_inputs=1)
class TimestampParts(
    NoFitTransformation, FixedOutputTransformation, SupportsPandas, SupportsSnowpark
):
    """Processes a timestamp column into its parts."""

    _time_part_functions: Dict[Enum, Dict[type, Callable]] = {
        DateTimeParts.DAY: {
            pd.DataFrame: lambda s: s.dt.day,
            snow.DataFrame: lambda s: snow.functions.dayofmonth(s),
        },
        DateTimeParts.MONTH: {
            pd.DataFrame: lambda s: s.dt.month,
            snow.DataFrame: lambda s: snow.functions.month(s),
        },
        DateTimeParts.YEAR: {
            pd.DataFrame: lambda s: s.dt.year,
            snow.DataFrame: lambda s: snow.functions.year(s),
        },
        DateTimeParts.HOUR: {
            pd.DataFrame: lambda s: s.dt.hour,
            snow.DataFrame: lambda s: snow.functions.hour(s),
        },
        DateTimeParts.MINUTE: {
            pd.DataFrame: lambda s: s.dt.minute,
            snow.DataFrame: lambda s: snow.functions.minute(s),
        },
        DateTimeParts.SECOND: {
            pd.DataFrame: lambda s: s.dt.second,
            snow.DataFrame: lambda s: snow.functions.second(s),
        },
        DateTimeParts.DAY_OF_WEEK: {
            pd.DataFrame: lambda s: (s.dt.dayofweek + 1) % 7,
            snow.DataFrame: lambda s: snow.functions.dayofweek(s),
        },
    }

    def __init__(self, inputs: Collection[str], **kwargs):
        """Initialize the timestamp parts operation.

        This operation processes a timestamp column into its parts.

        Args:
            inputs: The column name of the timestamp column.

        """
        super().__init__(inputs, **kwargs)

    @property
    def _data_type(self) -> Type[DataType]:
        return IntDataType

    def _transform_pandas(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply the timestamp parts operation to a pandas dataframe.

        Args:
            df: The data to transform.

        Returns:
            The transformed data.
        """
        [single_input] = self.input
        for part, part_label in self._output_parts.items():
            df[f"{self.name}{Transformation._output_delimiter}{part_label}"] = (
                self._time_part_functions[part][pd.DataFrame](
                    pd.to_datetime(df[single_input])
                )
            )
        return df

    def _transform_snowpark(self, df: snow.DataFrame) -> snow.DataFrame:
        """Apply the timestamp parts operation to a Snowpark dataframe.

        Args:
            df: The data to transform.

        Returns:
            The transformed data.
        """
        [single_input] = self.input
        for part, part_label in self._output_parts.items():
            df = df.with_column(
                double_quote(
                    f"{self.name}{Transformation._output_delimiter}{part_label}"
                ),
                self._time_part_functions[part][snow.DataFrame](
                    snow.functions.to_timestamp(df[double_quote(single_input)])
                ),
            )
        return df
