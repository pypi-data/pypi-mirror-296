from typing import Type

import pandas as pd
import snowflake.snowpark as snow

from tabpipe.data_types import DataType, FloatDataType
from tabpipe.dataframe.snowpark import double_quote
from tabpipe.transformations.transformation import (
    NoFitTransformation,
    SingleOutputTransformation,
    SupportsPandas,
    SupportsSnowpark,
    validate_inputs,
)


@validate_inputs(nr_inputs=1)
class Squared(
    NoFitTransformation, SingleOutputTransformation, SupportsPandas, SupportsSnowpark
):
    """A data transformations operation that squares the input data."""

    @property
    def _data_type(self) -> Type[DataType]:
        return FloatDataType

    def _transform_pandas(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply the squared operation to a pandas dataframe.

        Args:
            df: The data to transform.

        Returns:
            The transformed data.
        """
        [single_input] = self.input

        df[self.name] = df[single_input] ** 2

        return df

    def _transform_snowpark(self, df: snow.DataFrame) -> snow.DataFrame:
        """Apply the squared operation to a Snowpark dataframe.

        Args:
            df: The data to transform.

        Returns:
            The transformed data.
        """
        [single_input] = self.input

        df = df.with_column(
            double_quote(self.name), df[double_quote(single_input)] ** 2
        )

        return df
