from pandas.testing import assert_frame_equal
from snowflake.snowpark.testing import assert_dataframe_equal


def test_haversine_transform_pandas(
    haversine, base_locations_df, expected_locations_df
):
    """Test the transform_pandas method of the Squared operation."""
    result_df = haversine.transform(base_locations_df).dataframe
    assert assert_frame_equal(expected_locations_df, result_df, check_like=True) is None


def test_haversine_transform_snowpark(
    snowflake_connection, haversine, base_locations_df, expected_locations_df
):
    """Test the transform_snowpark method of the Squared operation."""
    base_df = snowflake_connection.create_dataframe(base_locations_df)
    expected_df = snowflake_connection.create_dataframe(expected_locations_df)

    result_df = haversine.transform(base_df).dataframe
    try:
        assert_dataframe_equal(expected_df, result_df)
    except AssertionError as e:
        assert False, e
