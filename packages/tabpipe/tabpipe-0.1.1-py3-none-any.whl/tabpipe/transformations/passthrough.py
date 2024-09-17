from typing import List, Type

import pandas as pd
import snowflake.snowpark as snow

from tabpipe.data_types import DataType, FloatOrString
from tabpipe.dataframe.snowpark import double_quote
from tabpipe.transformations.transformation import (
    NoFitTransformation,
    SingleOutputTransformation,
    SupportsPandas,
    SupportsSnowpark,
    validate_inputs,
)


@validate_inputs(nr_inputs=1, enclose_input_name=False)
class PassThrough(
    NoFitTransformation, SingleOutputTransformation, SupportsPandas, SupportsSnowpark
):
    """A pass-through operation that keeps the data as is."""

    def __init__(
        self,
        inputs: List[str],
        data_type: Type[DataType] = FloatOrString,
        **kwargs,
    ):
        """Initialize the pass-through operation.

        This operation keeps the data as is.

        Args:
            inputs: The column name of the input data.
            data_type: The data type of the output data.
        """
        self._data_type_ = data_type
        super().__init__(inputs, **kwargs)

    @property
    def _data_type(self) -> Type[DataType]:
        """Return the data type of the output data."""
        return self._data_type_

    def _transform_pandas(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply the pass-through operation to a pandas dataframe.

        The only effect is to rename the columns according to the feature name.

        Args:
            df: The data to transform.

        Returns:
            The transformed data.
        """
        [single_input] = self.input

        return df.rename(columns={single_input: self.name})

    def _transform_snowpark(self, df: snow.DataFrame) -> snow.DataFrame:
        """Apply the pass-through operation to a Snowpark dataframe.

        The only effect is to rename the columns according to the feature name.

        Args:
            df: The data to transform.

        Returns:
            The transformed data.
        """
        [single_input] = self.input

        return df.rename({double_quote(single_input): double_quote(self.name)})
