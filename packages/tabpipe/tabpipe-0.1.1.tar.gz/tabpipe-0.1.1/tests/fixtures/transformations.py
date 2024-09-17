"""This module contains transformations for testing.

Each transformation should have corresponding fixtures that provide:
- Data for it to transform
- The expected output of the transformation of that data
"""

import pandas as pd
import pytest

from tabpipe.transformations import (
    Haversine,
    ListCategorical,
    PassThrough,
    Squared,
    TimestampParts,
)
from tabpipe.units import DateTimeParts


# Input ################################################################################
@pytest.fixture()
def passthrough_transformation():
    """Create an Input transformation for testing."""
    transformation = PassThrough(["a"])
    return transformation


@pytest.fixture
def passthrough_expected_df(base_df, passthrough_transformation):
    """Create an expected dataframe for testing."""
    [single_input] = passthrough_transformation.input

    return base_df.rename(
        columns={single_input: passthrough_transformation.name}
    ).astype({single_input: float})


# Squared ##############################################################################
@pytest.fixture()
def squared():
    """Create a squared transformation for testing."""
    transformation = Squared(["a"], name="a_squared")
    return transformation


@pytest.fixture()
def squared_expected_df(base_df, squared):
    """Create an expected dataframe for testing."""
    return pd.concat(
        [
            base_df,
            pd.DataFrame({squared.name: map(float, [1, 16, 49])}),
        ],
        axis=1,
    )


# TimestampParts #######################################################################
@pytest.fixture(scope="module")
def timestamp_parts_1():
    """Create a squared transformation for testing."""
    transformation = TimestampParts(
        ["timestamp_1"],
        output_parts=[
            DateTimeParts.YEAR,
            DateTimeParts.MONTH,
            DateTimeParts.DAY,
            DateTimeParts.HOUR,
            DateTimeParts.MINUTE,
            DateTimeParts.SECOND,
            DateTimeParts.DAY_OF_WEEK,
        ],
    )
    return transformation


@pytest.fixture()
def expected_timestamps_df1(timestamp_parts_1, base_timestamps_df):
    """Create an expected dataframe for testing."""
    return pd.concat(
        [
            base_timestamps_df,
            pd.DataFrame(
                {
                    f"{timestamp_parts_1.name}.year": [2020, 2020, 2000],
                    f"{timestamp_parts_1.name}.month": [1, 2, 12],
                    f"{timestamp_parts_1.name}.day": [1, 1, 12],
                    f"{timestamp_parts_1.name}.hour": [16, 0, 12],
                    f"{timestamp_parts_1.name}.minute": [20, 0, 34],
                    f"{timestamp_parts_1.name}.second": [0, 0, 56],
                    f"{timestamp_parts_1.name}.day_of_week": [3, 6, 2],
                }
            ),
        ],
        axis=1,
    )


@pytest.fixture()
def timestamp_parts_2():
    """Create a squared transformation for testing."""
    transformation = TimestampParts(
        ["timestamp_2"],
        output_parts=[
            DateTimeParts.YEAR,
            DateTimeParts.MONTH,
            DateTimeParts.DAY,
            DateTimeParts.DAY_OF_WEEK,
        ],
    )
    return transformation


@pytest.fixture()
def expected_timestamps_df2(timestamp_parts_2, base_timestamps_df):
    """Create an expected dataframe for testing."""
    return pd.concat(
        [
            base_timestamps_df,
            pd.DataFrame(
                {
                    f"{timestamp_parts_2.name}.year": [2020, 2022, 2024],
                    f"{timestamp_parts_2.name}.month": [1, 8, 8],
                    f"{timestamp_parts_2.name}.day": [1, 16, 1],
                    f"{timestamp_parts_2.name}.day_of_week": [3, 2, 4],
                }
            ),
        ],
        axis=1,
    )


# Haversine ############################################################################
@pytest.fixture()
def haversine():
    """Create a squared transformation for testing."""
    transformation = Haversine(["lat_x", "lon_x", "lat_y", "lon_y"])
    return transformation


@pytest.fixture()
def expected_locations_df(haversine, base_locations_df):
    """Create an expected dataframe for testing."""
    return pd.concat(
        [
            base_locations_df,
            pd.DataFrame({haversine.name: [8295.062182, 9716.962915, 6651.688144]}),
        ],
        axis=1,
    )


# ListCategorical ######################################################################
@pytest.fixture(scope="module")
def list_categorical_1():
    """Create a ListCategorical transformation for testing."""
    transformation = ListCategorical(
        ["fruits"],
        min_frequency=0.5,
    )
    return transformation


@pytest.fixture()
def expected_list_categorical_df1(list_categorical_1, base_list_categorical_df):
    """Create an expected dataframe for testing."""
    return pd.concat(
        [
            base_list_categorical_df,
            pd.DataFrame(
                {
                    f"{list_categorical_1.name}.apple": [True, True, False, True],
                    f"{list_categorical_1.name}.banana": [True, True, False, False],
                    f"{list_categorical_1.name}.cherry": [True, False, True, True],
                }
            ),
        ],
        axis=1,
    )


@pytest.fixture()
def list_categorical_2():
    """Create a ListCategorical transformation for testing."""
    transformation = ListCategorical(
        ["fruits_strings"],
    )
    return transformation


@pytest.fixture()
def expected_list_categorical_df2(list_categorical_2, base_list_categorical_df):
    """Create an expected dataframe for testing."""
    return pd.concat(
        [
            base_list_categorical_df,
            pd.DataFrame(
                {
                    f"{list_categorical_2.name}.apple": [True, False, False, False],
                    f"{list_categorical_2.name}.banana": [True, False, False, False],
                    f"{list_categorical_2.name}.cherry": [True, False, False, False],
                }
            ),
        ],
        axis=1,
    )
