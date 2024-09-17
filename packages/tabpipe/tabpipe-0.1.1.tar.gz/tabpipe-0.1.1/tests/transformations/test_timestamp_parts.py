from pandas.testing import assert_frame_equal
from snowflake.snowpark.testing import assert_dataframe_equal


def test_timestamp_parts_transform_pandas1(
    base_timestamps_df, expected_timestamps_df1, timestamp_parts_1
):
    """Test the transform_pandas method of the Squared operation."""
    result_df = timestamp_parts_1.transform(base_timestamps_df).dataframe
    assert (
        assert_frame_equal(expected_timestamps_df1, result_df, check_like=True) is None
    )


def test_timestamp_parts_transform_pandas2(
    base_timestamps_df, expected_timestamps_df2, timestamp_parts_2
):
    """Test the transform_pandas method of the Squared operation."""
    result_df = timestamp_parts_2.transform(base_timestamps_df).dataframe
    assert (
        assert_frame_equal(expected_timestamps_df2, result_df, check_like=True) is None
    )


def test_timestamp_parts_transform_snowpark1(
    snowflake_connection,
    base_timestamps_df_snowpark,
    timestamp_parts_1,
    expected_timestamps_df1,
):
    """Test the transform_snowpark method of the Squared operation."""
    expected_snow_df = snowflake_connection.create_dataframe(expected_timestamps_df1)

    result_df = timestamp_parts_1.transform(base_timestamps_df_snowpark).dataframe
    try:
        assert_dataframe_equal(expected_snow_df, result_df)
    except AssertionError as e:
        assert False, e


def test_timestamp_parts_transform_snowpark2(
    snowflake_connection,
    base_timestamps_df_snowpark,
    timestamp_parts_2,
    expected_timestamps_df2,
):
    """Test the transform_snowpark method of the Squared operation."""
    expected_snow_df = snowflake_connection.create_dataframe(expected_timestamps_df2)

    result_df = timestamp_parts_2.transform(base_timestamps_df_snowpark).dataframe
    try:
        assert_dataframe_equal(expected_snow_df, result_df)
    except AssertionError as e:
        assert False, e
