"""This module contains pipelines for testing.

Each pipeline should have corresponding fixtures that provide:
- Data for it to transform
- The expected output of the transformation of that data using the pipeline
"""

import pandas as pd
import pytest

from tabpipe import Pipeline
from tabpipe.transformations import Squared


@pytest.fixture()
def pipeline_1(
    passthrough_transformation,
    squared,
    haversine,
    list_categorical_1,
    timestamp_parts_1,
):
    """Return a Pipeline instance.

    Reuse transformation fixtures from the transformations tests.
    """
    return Pipeline(
        [
            passthrough_transformation,
            squared,
            haversine,
            list_categorical_1,
            timestamp_parts_1,
            Squared(
                [out.name for out in passthrough_transformation.output],
                name="passthrough_squared",
            ),
            Squared([out.name for out in squared.output], name="squared_squared"),
        ]
    )


@pytest.fixture()
def fitted_pipeline_1(pipeline_1, base_df):
    """Fit the pipeline instance."""
    pipeline_1.fit(base_df)

    return pipeline_1


@pytest.fixture()
def expected_transformed_base_df_pipeline_1_pandas(
    n_rows,
    passthrough_expected_df,
    squared_expected_df,
    expected_locations_df,
    expected_list_categorical_df1,
    expected_timestamps_df1,
):
    """Create an expected dataframe for testing."""
    df = pd.concat(
        [
            passthrough_expected_df.head(n_rows),
            squared_expected_df.head(n_rows),
            expected_locations_df.head(n_rows),
            expected_list_categorical_df1.head(n_rows),
            expected_timestamps_df1.head(n_rows),
            pd.DataFrame(
                {
                    "passthrough_squared": map(float, [1, 16, 49]),
                    "squared_squared": map(float, [1, 256, 2401]),
                }
            ).head(n_rows),
        ],
        axis=1,
    )

    return df.loc[:, ~df.columns.duplicated()].filter(
        [
            "a",
            "a_squared",
            "Haversine",
            "ListCategorical(fruits).apple",
            "ListCategorical(fruits).banana",
            "ListCategorical(fruits).cherry",
            "ListCategorical(fruits).orange",
            "TimestampParts(timestamp_1).year",
            "TimestampParts(timestamp_1).month",
            "TimestampParts(timestamp_1).day",
            "TimestampParts(timestamp_1).hour",
            "TimestampParts(timestamp_1).minute",
            "TimestampParts(timestamp_1).second",
            "TimestampParts(timestamp_1).day_of_week",
            "passthrough_squared",
            "squared_squared",
        ],
        axis=1,
    )


@pytest.fixture()
def expected_transformed_base_df_pipeline_1_snowpark(
    snowflake_connection,
    expected_transformed_base_df_pipeline_1_pandas,
):
    """Create an expected dataframe for testing."""
    return snowflake_connection.create_dataframe(
        expected_transformed_base_df_pipeline_1_pandas
    )
