"""Data types for the tabpipe package.

For pandas-snowflake equivalence, see:
https://docs.snowflake.com/en/developer-guide/snowpark/python/snowpark-pandas#data-types
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Type

import numpy as np
import snowflake.snowpark as snow
from typing_extensions import Self


class DataType(ABC):
    """Abstract class for data types."""

    _precision: Optional[int] = None
    _compatibles: Optional[List[type]] = None

    @property
    @abstractmethod
    def pandas_type(self):
        """The pandas data type corresponding to the data type.

        Returns:
            The pandas data type.
        """
        pass

    @property
    @abstractmethod
    def snowpark_type(self):
        """The Snowpark data type corresponding to the data type.

        Returns:
            The Snowpark data type.
        """
        pass

    @classmethod
    def get_precision(cls) -> Optional[int]:
        """The precision of the data type.

        Returns:
            The precision of the data type.
        """
        return cls._precision

    @classmethod
    def get_compatibles(cls) -> List[Type[Self]]:
        """Get the compatible data types.

        Returns:
            The compatible data types.
        """
        if cls._compatibles is None:
            return [cls]

        return cls._compatibles


class NumericDataType(DataType, ABC):
    """Numeric data type."""

    pass


class IntDataType(NumericDataType):
    """Integer data type."""

    pandas_type = np.int64
    snowpark_type = snow.types.IntegerType()


class FloatDataType(NumericDataType):
    """Float data type."""

    _precision = 6
    pandas_type = np.float64
    snowpark_type = snow.types.FloatType()


class StringDataType(DataType):
    """String data type."""

    pandas_type = str
    snowpark_type = snow.types.StringType()


class BoolDataType(DataType):
    """Boolean data type."""

    pandas_type = bool
    snowpark_type = snow.types.BooleanType()


class DatetimeDataType(DataType):
    """Datetime data type."""

    pandas_type = np.datetime64
    snowpark_type = snow.types.TimestampType()


class ObjectDataType(DataType):
    """Object data type."""

    pandas_type = object
    snowpark_type = snow.types.VariantType()


class FloatOrString(DataType, ABC):
    """A data type that is inferred from the data."""

    _compatibles = [FloatDataType, StringDataType]
