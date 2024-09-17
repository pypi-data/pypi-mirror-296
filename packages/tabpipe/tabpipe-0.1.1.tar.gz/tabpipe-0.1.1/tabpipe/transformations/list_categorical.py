from ast import literal_eval
from collections import Counter
from collections.abc import Iterable
from typing import Collection, Dict, List, Type

import numpy as np
import pandas as pd
import snowflake.snowpark as snow

from tabpipe.data_types import BoolDataType, DataType
from tabpipe.dataframe.snowpark import double_quote
from tabpipe.feature import Feature
from tabpipe.transformations.transformation import (
    SupportsPandas,
    SupportsSnowpark,
    validate_inputs,
)
from tabpipe.utils.strings import snake_case


def try_parse_list(lst: str) -> List:
    """Tries to parse a list from a string.

    Args:
        lst: The list to parse.

    Returns:
        The parsed list.
    """
    try:
        return literal_eval(lst.replace("null", "None"))
    except (ValueError, SyntaxError):
        return []


@validate_inputs(nr_inputs=1)
class ListCategorical(SupportsPandas, SupportsSnowpark):
    """Processes a timestamp column into its parts."""

    def __init__(self, inputs: Collection[str], min_frequency: float = 0.01, **kwargs):
        """Initialize the timestamp parts operation.

        This operation processes a timestamp column into its parts.

        Args:
            inputs: The column name of the timestamp column.
            min_frequency: The minimum frequency of a category to be considered.

        """
        super().__init__(inputs, **kwargs)
        self._min_frequency = min_frequency
        self._categories: Dict[str, int] = {}

    @property
    def _data_type(self) -> Type[DataType]:
        return BoolDataType

    def _finalize_fit(self, counts: Counter, threshold: int) -> None:
        idx = 0
        for category, occurrences in counts.items():
            if occurrences >= threshold:
                self._categories[category] = idx
                idx += 1

        self._output: List[Feature] = [
            Feature(
                f"{self.name}{self._output_delimiter}{snake_case(category)}",
                f"Whether the category '{category}' is present in {self._input}",
                self._data_type,
            )
            for category in sorted(self._categories, key=lambda x: self._categories[x])
        ]

    def _fit_pandas(self, df: pd.DataFrame) -> None:
        """Fit a Pandas dataframe."""
        [input_col] = self.input

        # Parse lists in input column
        # and count the occurrences of each unique value in the lists
        counts: Counter = Counter()
        seen_strings: Dict[str, Iterable] = {}
        for obj in df[input_col]:
            if isinstance(obj, str):
                # Instead of parsing the same string multiple times,
                # we parse it once and store the result in a hash table
                if obj in seen_strings:
                    parsed = seen_strings[obj]
                else:
                    parsed = try_parse_list(obj)
                    seen_strings[obj] = parsed
            elif isinstance(obj, Iterable):
                parsed = obj
            else:
                parsed = []

            counts.update(parsed)

        self._finalize_fit(counts, int(self._min_frequency * len(df)))

    def _fit_snowpark(self, df: snow.DataFrame) -> None:
        """Fit a Snowpark dataframe."""
        [input_col] = self.input
        quoted_input_col = double_quote(input_col)

        # Parse input column
        category_col = "CATEGORY"
        occurrences_col = "OCCURRENCES"

        flattened = df.join_table_function(
            snow.functions.flatten(
                snow.functions.function("try_parse_json")(df[quoted_input_col])
            ).alias("seq", "key", "path", "idx", category_col, "this")
        )
        grouped = flattened.group_by(flattened[category_col])
        counts = grouped.count()
        counts = counts.with_column_renamed("COUNT", occurrences_col).with_column(
            category_col,
            snow.functions.to_varchar(counts[category_col]),
        )

        local_counts = Counter(
            {
                row[category_col]: row[occurrences_col]
                for row in counts.to_local_iterator()
            }
        )

        self._finalize_fit(local_counts, int(self._min_frequency * df.count()))

    def _transform_pandas(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform a Pandas dataframe."""
        [input_col] = self.input

        # Create array of zeros
        dummy_array = np.zeros((len(df), len(self._categories)), dtype=bool)

        # Parse lists in input column
        # and set the corresponding dummy variables to True
        seen_strings: Dict[str, Iterable] = {}
        for i, obj in enumerate(df[input_col]):
            # Same caching strategy as in the fit method
            if isinstance(obj, str):
                if obj in seen_strings:
                    parsed = seen_strings[obj]
                else:
                    parsed = try_parse_list(obj)
                    seen_strings[obj] = parsed
            elif isinstance(obj, Iterable):
                parsed = obj
            else:
                parsed = []

            dummy_idx = [
                self._categories[category]
                for category in parsed
                if category in self._categories
            ]
            dummy_array[i, dummy_idx] = True

        # Add output columns to dataframe
        for category, idx in self._categories.items():
            df[self._output[idx].name] = dummy_array[:, idx]  # type: ignore # only runs if fit

        return df

    def _transform_snowpark(self, df: snow.DataFrame) -> snow.DataFrame:
        """Transform a Snowpark dataframe."""
        [input_col] = self.input
        quoted_input_col = double_quote(input_col)

        for category in self._categories:
            df = df.with_column(
                double_quote(self._output[self._categories[category]].name),
                snow.functions.coalesce(
                    snow.functions.array_contains(
                        snow.functions.to_variant(snow.functions.lit(category)),
                        snow.functions.function("try_parse_json")(df[quoted_input_col]),
                    ),
                    snow.functions.lit(False),
                ),
            )

        return df
