from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Callable, Collection, Dict, List, Optional, Type, Union

import pandas as pd
import snowflake.snowpark as snow

from tabpipe.data_types import DataType
from tabpipe.dataframe import DataFrame
from tabpipe.exceptions import NotFittedError
from tabpipe.feature import Feature


class Transformation(ABC):
    """A data transformations operation that can be applied to a dataframe.

    This is the basic unit of how we define data transformations in tabpipe.

    This class defines the basic behavior of a data transformations operation,
    and it can be extended to implement the actual transformation logic.

    The subclasses should override the `fit_*` and `transform_*` methods to implement
    the actual transformation logic - although that is not mandatory as one might
    choose to develop a data transformation that isn't expected to run in a
    specific environment.
    """

    _output_delimiter: str = "."
    _disallowed_name_chars = [' ', _output_delimiter, '"']
    _fit_mapping: Dict[Type, Callable]
    _transform_mapping: Dict[Type, Callable]

    def __init__(
        self,
        inputs: Collection[str],
        input_types: Optional[Collection[type]] = None,
        name: Optional[str] = None,
    ) -> None:
        """Initialize a data transformations operation.

        Args:
            inputs: The columns that the operation will use as input.
            input_types: The types of the inputs. Should have the same length as inputs.
                By default, all inputs are assumed to be columns present in the dataframe (Feature).
                If the inputs types are specified as Transformation, they're expected to
                be the output of a previous transformation, in which case the Pipeline
                containing this transformation should later set its input to be the
                output of the previous transformation, once we know what it is.
            name: The name of the operation.
        """
        if input_types is None:
            input_types = [Feature] * len(inputs)

        self._input_types = list(input_types)
        self._resolved_input_types = all(it == Feature for it in self._input_types)
        self.input: List = list(inputs)
        self._name: str = self.__class__.__name__ if name is None else name
        self._output: Optional[List[Feature]] = None
        self._is_fit = False
        self._has_known_output = False

    @classmethod
    def __init_subclass__(cls, **kwargs) -> None:
        """Initialize the subclass."""
        super().__init_subclass__(**kwargs)

        cls._transform_mapping = {}
        cls._fit_mapping = {}

    @property
    @abstractmethod
    def _data_type(self) -> Union[List[Type[DataType]], Type[DataType]]:
        """The data type of the transformation output."""
        pass

    def _get_data_type(self, output_shaped: List):
        if isinstance(self._data_type, list):
            if len(self._data_type) != len(output_shaped):
                raise ValueError(
                    f"Number of data types ({len(self._data_type)}) does not match number of outputs ({len(output_shaped)})"
                )
            return self._data_type
        elif isinstance(self._data_type, type):
            if issubclass(self._data_type, DataType):
                return [self._data_type] * len(output_shaped)

        raise ValueError(f"Invalid data type: {self._data_type}")

    @property
    def data_type(self) -> List[Type[DataType]]:
        """The data type of the transformation output."""
        return self._get_data_type(self.output)

    @property
    def input_types(self) -> List[Type]:
        """The data type of the transformation input."""
        return self._input_types

    @input_types.setter
    def input_types(self, input_types: Collection[Type]) -> None:
        """Set the input types for the operation."""
        if len(input_types) != len(self._input):
            raise ValueError("Number of input types should match number of inputs")
        self._input_types = list(input_types)

        if any(
            isinstance(input_type, Transformation) for input_type in self._input_types
        ):
            self._resolved_input_types = False
        else:
            self._resolved_input_types = True

    @property
    def resolved_input_types(self) -> bool:
        """Whether the input types have been resolved."""
        return self._resolved_input_types

    @property
    def has_known_output(self) -> bool:
        """Whether the output of the transformation is known."""
        return self._has_known_output

    @has_known_output.setter
    def has_known_output(self, has_known_output: bool) -> None:
        """Set whether the output of the transformation is known."""
        self._has_known_output = has_known_output

    def _validate_inputs(self, inputs: Collection[str]) -> None:
        """Validate the input columns for the operation."""
        if not self.resolved_input_types:
            return

        pass

    @property
    def input(self) -> List[str]:
        """Get the input columns for the operation."""
        return self._input

    @input.setter
    def input(self, inputs: Collection[str]) -> None:
        """Set the input columns for the operation."""
        self._validate_inputs(inputs)
        self._input = list(inputs)

    @property
    def name(self) -> str:
        """Get the feature name for the operation."""
        if self._name is None:
            raise ValueError("Feature name not set")
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """Set the feature name for the operation."""
        self._name = name

    @property
    def output(self) -> List[Feature]:
        """Get the output columns for the operation."""
        if self._output is None:
            raise ValueError("Transformation output not set")

        return self._output

    def transform(self, df: object) -> DataFrame:
        """Apply the data transformations operation to a dataframe.

        The underlying implementation to use is determined by the type of the dataframe.

        Args:
            df: The data to transform.

        Returns:
            The transformed data.

        Raises:
            NotFittedError: If the dataframe type is not supported.
        """
        if not self._is_fit:
            raise NotFittedError(self)

        df = DataFrame.from_object(df)
        df.check_columns(self.input)
        transformed = self._transform_mapping[df.dataframe_type()](self, df.dataframe)
        transformed = DataFrame.from_object(transformed)

        return self.format_output(transformed)

    def format_output(self, df: DataFrame) -> DataFrame:
        """Apply post-transformations to the output of the data transformations operation.

        Args:
            df: The data to format.

        Returns:
            The formatted data.
        """
        df.check_columns([f.name for f in self.output])
        for f in self.output:
            df = df.format_column(f.name, f.data_type)

        return df

    def fit(self, df: Any) -> None:
        """Fit the data transformations operation to the data.

        The underlying implementation to use is determined by the type of the dataframe.

        Args:
            df: The data to fit the operation to.

        Raises:
            ValueError: If the dataframe type is not supported.
        """
        df = DataFrame.from_object(df)
        df.check_columns(self.input)
        self._fit_mapping[df.dataframe_type()](self, df.dataframe)

        self._is_fit = True

    def fit_transform(self, df: Any) -> DataFrame:
        """Fit the data transformations operation to the data and transform it.

        Args:
            df: The data to fit the operation to and transform.

        Returns:
            The transformed data.
        """
        self.fit(df)
        return self.transform(df)


class NoFitTransformation(Transformation, ABC):
    """A data transformations operation that does not require fitting.

    This is a convenience class for operations that do not require fitting.
    """

    def __init__(self, *args, **kwargs):
        """Initialize a data transformations operation that does not require fitting."""
        super().__init__(*args, **kwargs)
        self._is_fit = True
        self._has_known_output = True

    def fit(self, df: Any) -> None:
        """Override the fit method to do nothing.

        Args:
            df: The dataframe passed to the fit method.
        """
        pass


def validate_inputs(
    nr_inputs: Optional[int] = None,
    enclose_input_name: bool = True,
):
    """Produces a decorator that validates inputs to DataProcessing implementations.

    Keyword Args:
        nr_inputs: The number of inputs that the data transformations operation expects.
        enclose_input_name: Whether to enclose the input name in parentheses
            (only when nr_inputs=1 and name is not provided).

    Returns:
        A decorator that validates the number of inputs to a data transformations operation.

    Raises:
        ValueError: If the decorated class is not a subclass of DataProcessing.
    """

    def _validate_inputs_decorator(cls: type):
        """A decorator that validates inputs to DataProcessing implementations."""
        if not issubclass(cls, Transformation):
            raise ValueError(f"{cls} must be a subclass of Transformation")

        # Store the original methods
        original_init = cls.__init__
        original_validate_inputs = cls._validate_inputs

        name_arg = "name"

        def _new_init(self, inputs, *args, **kwargs):
            if nr_inputs == 1 and name_arg not in kwargs:
                [kwargs[name_arg]] = inputs

                if enclose_input_name:
                    kwargs[name_arg] = f"{cls.__name__}({kwargs[name_arg]})"

            original_init(self, inputs, *args, **kwargs)

        def _new_validate_inputs(self, inputs: Collection[str]) -> None:
            """Validate the input columns for the operation."""
            if nr_inputs is not None and len(inputs) != nr_inputs:
                raise ValueError(
                    f"{cls} expected {nr_inputs} inputs, got {len(inputs)}"
                )

            original_validate_inputs(self, inputs)

        # Override the original methods
        cls.__init__ = _new_init  # type: ignore
        cls._validate_inputs = _new_validate_inputs  # type: ignore

        return cls

    return _validate_inputs_decorator


class FixedOutputTransformation(Transformation, ABC):
    """A mixin class for data transformations operations that have a fixed output."""

    def __init__(
        self,
        inputs: Collection[str],
        output_parts: Union[List[Enum], Dict[Enum, str]],
        **kwargs,
    ):
        """Initialize a transformation with fixed output parts."""
        super().__init__(inputs, **kwargs)

        if isinstance(output_parts, list):
            output_parts = {i: i.value for i in output_parts}
        elif not isinstance(output_parts, dict):
            raise ValueError(
                f"`output_parts` must be a list or dict, got {type(output_parts)}"
            )

        self._output_parts: Dict[Enum, str] = output_parts
        data_types = self._get_data_type(list(self._output_parts))

        self._output = [
            Feature(
                f"{self.name}{self._output_delimiter}{self._output_parts[part]}",
                f"Part '{part}' of the {self.name} transformation on columns {self.input}",
                data_types[i],
            )
            for i, part in enumerate(self._output_parts)
        ]


class SingleOutputTransformation(FixedOutputTransformation, ABC):
    """A mixin class for data transformations operations that have a single output."""

    _output_delimiter = ""

    def __init__(self, inputs: Collection[str], **kwargs):
        """Initialize a transformation with single output."""

        class SinglePart(Enum):
            """An enumeration of the single output part."""

            single_part = ""

        super().__init__(inputs, [SinglePart.single_part], **kwargs)


"""
In the interfaces below, we use NotImplementedError instead of `abstractmethod` to
allow for more flexibility in the implementation of the subclasses, for example in the way
they interact with the `NoFitTransformation` mixin class.

If these were to be implemented as abstract methods, the subclasses would have to inherit
from the `NoFitTransformation` AFTER the other interfaces (e.g. `SupportsPandas`), and we
don't want the user to have to worry about that sort of thing.
"""


class SupportsPandas(Transformation, ABC):
    """A mixin class for data transformations operations that support Pandas dataframes."""

    @classmethod
    def __init_subclass__(cls, **kwargs):
        """Initialize the subclass."""
        super().__init_subclass__(**kwargs)

        cls._transform_mapping[pd.DataFrame] = cls._transform_pandas
        cls._fit_mapping[pd.DataFrame] = cls._fit_pandas

    def _fit_pandas(self, dataframe: pd.DataFrame) -> None:
        """Fit a Pandas dataframe."""
        raise NotImplementedError

    def _transform_pandas(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """Transform a Pandas dataframe."""
        raise NotImplementedError


class SupportsSnowpark(Transformation, ABC):
    """A mixin class for data transformations operations that support Snowpark dataframes."""

    @classmethod
    def __init_subclass__(cls, *args, **kwargs):
        """Initialize the subclass."""
        super().__init_subclass__(*args, **kwargs)

        cls._transform_mapping[snow.DataFrame] = cls._transform_snowpark
        cls._fit_mapping[snow.DataFrame] = cls._fit_snowpark

    def _fit_snowpark(self, dataframe: snow.DataFrame) -> None:
        """Fit a Snowpark dataframe."""
        raise NotImplementedError

    @abstractmethod
    def _transform_snowpark(self, dataframe: snow.DataFrame) -> snow.DataFrame:
        """Transform a Snowpark dataframe."""
        raise NotImplementedError
