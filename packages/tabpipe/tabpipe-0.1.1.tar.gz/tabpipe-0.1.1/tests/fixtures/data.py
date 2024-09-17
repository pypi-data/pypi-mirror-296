"""This module contains data for testing."""

import pandas as pd
import pytest
import snowflake.snowpark as snow


@pytest.fixture()
def n_rows():
    """Return the number of rows for testing.

    This is used to guarantee that when we're concatenating dataframes coming from
    different fixtures, we match the number of rows.
    """
    return 3


@pytest.fixture()
def base_locations_df():
    """Create a base dataframe for testing."""
    return pd.DataFrame(
        {
            "lat_x": [41.560201, 48.8584, 40.7484],
            "lon_x": [-8.413651, 2.2945, 73.9857],
            "lat_y": [13.1632, 35.7101, 33.8568],
            "lon_y": [72.5453, 139.8107, 151.2153],
        }
    )


@pytest.fixture()
def base_list_categorical_df():
    """Create a base dataframe for testing."""
    return pd.DataFrame(
        {
            "fruits": [
                ["apple", "banana", "cherry"],
                ["apple", "banana"],
                ["cherry"],
                ["apple", "orange", "cherry"],
            ],
            "fruits_strings": [
                '["apple", "banana", "cherry"]',
                'bad format',
                None,
                '["fruit, "aaa1"]',
            ],
        }
    )


@pytest.fixture()
def base_list_categorical_snowpark_df(
    snowflake_connection, base_list_categorical_df
) -> snow.DataFrame:
    """Create a base dataframe for testing."""
    return snowflake_connection.create_dataframe(base_list_categorical_df)


@pytest.fixture()
def base_timestamps_df():
    """Create a base dataframe for testing."""
    return pd.DataFrame(
        {
            "timestamp_1": pd.to_datetime(
                [
                    "2020-01-01 16:20:00.000",
                    "2020-02-01 00:00:00.000",
                    "2000-12-12 12:34:56.000",
                ]
            ),
            "timestamp_2": ["2020-01-01", "2022-08-16", "2024-08-01"],
        }
    )


@pytest.fixture()
def base_timestamps_df_snowpark(
    snowflake_connection, base_timestamps_df
) -> snow.DataFrame:
    """Create a base dataframe for testing."""
    return snowflake_connection.create_dataframe(base_timestamps_df)


@pytest.fixture()
def base_df(
    n_rows,
    base_locations_df,
    base_list_categorical_df,
    base_timestamps_df,
) -> pd.DataFrame:
    """Create a base dataframe for testing."""
    return pd.concat(
        [
            pd.DataFrame(
                {
                    # Basic columns
                    "a": [1, 4, 7],
                    "b": [2, 5, 8],
                    "c": [3, 6, 9],
                }
            ),
            base_locations_df.head(n_rows),
            base_list_categorical_df.head(n_rows),
            base_timestamps_df.head(n_rows),
        ],
        axis=1,
    )


@pytest.fixture()
def base_df_snowpark(snowflake_connection, base_df) -> snow.DataFrame:
    """Create a base dataframe for testing."""
    return snowflake_connection.create_dataframe(base_df)
