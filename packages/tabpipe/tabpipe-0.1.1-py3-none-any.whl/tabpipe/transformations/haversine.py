from typing import Collection, Type

import numpy as np
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
from tabpipe.units import DistanceUnits


@validate_inputs(nr_inputs=4)
class Haversine(
    NoFitTransformation, SingleOutputTransformation, SupportsPandas, SupportsSnowpark
):
    """Calculates the haversine distance between two points."""

    def __init__(
        self,
        inputs: Collection[str],
        distance_unit: DistanceUnits = DistanceUnits.KILOMETERS,
        **kwargs,
    ):
        """Initialize the haversine operation.

        This operation calculates the haversine distance between two points X and Y.

        Args:
            inputs: Exactly 4 column names which are respectively:
                [latitude_x, longitude_x, latitude_y, longitude_y].
            distance_unit: The unit of distance to use.

        Raises:
            ValueError: If the number of inputs is not 4.
        """
        super().__init__(inputs, **kwargs)
        self._distance_unit = distance_unit
        self._earth_radius = 6371000 / self._distance_unit.value
        self._latitude_x, self._longitude_x, self._latitude_y, self._longitude_y = (
            inputs
        )

    @property
    def _data_type(self) -> Type[DataType]:
        return FloatDataType

    def _transform_pandas(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply the haversine operation to a pandas dataframe.

        Args:
            df: The data to transform.

        Returns:
            The transformed data.
        """
        # Convert latitude and longitude from degrees to radians
        radians_lat_x, radians_lon_x, radians_lat_y, radians_lon_y = [
            df[c] * np.pi / 180
            for c in (
                self._latitude_x,
                self._longitude_x,
                self._latitude_y,
                self._longitude_y,
            )
        ]

        # Calculate the haversine distance
        df[self.name] = (
            2
            * self._earth_radius
            * np.arcsin(
                np.sqrt(
                    np.sin((radians_lat_y - radians_lat_x) / 2) ** 2
                    + np.cos(radians_lat_x)
                    * np.cos(radians_lat_y)
                    * np.sin((radians_lon_y - radians_lon_x) / 2) ** 2
                )
            )
        )

        return df

    def _transform_snowpark(self, df: snow.DataFrame) -> snow.DataFrame:
        """Apply the haversine operation to a Snowpark dataframe.

        Args:
            df: The data to transform.

        Returns:
            The transformed data.
        """
        radians_lat_x, radians_lon_x, radians_lat_y, radians_lon_y = [
            # Snowpark API does not have a constant for pi
            df[double_quote(c)] * 3.141592653589793 / 180
            for c in (
                self._latitude_x,
                self._longitude_x,
                self._latitude_y,
                self._longitude_y,
            )
        ]

        # Calculate the haversine distance
        df = df.with_column(
            double_quote(self.name),
            2
            * self._earth_radius
            * snow.functions.asin(
                snow.functions.sqrt(
                    snow.functions.pow(
                        snow.functions.sin((radians_lat_y - radians_lat_x) / 2),
                        2,
                    )
                    + snow.functions.cos(radians_lat_x)
                    * snow.functions.cos(radians_lat_y)
                    * snow.functions.pow(
                        snow.functions.sin((radians_lon_y - radians_lon_x) / 2),
                        2,
                    )
                )
            ),
        )

        return df
