from pandas.testing import assert_frame_equal
from snowflake.snowpark.testing import assert_dataframe_equal


def test_squared_transform_pandas(base_df, squared_expected_df, squared):
    """Test the transform_pandas method of the Squared operation."""
    result_df = squared.transform(base_df).dataframe
    assert assert_frame_equal(squared_expected_df, result_df, check_like=True) is None


def test_squared_transform_snowpark(
    snowflake_connection, base_df_snowpark, squared, squared_expected_df
):
    """Test the transform_snowpark method of the Squared operation."""
    expected_snow_df = snowflake_connection.create_dataframe(squared_expected_df)

    result_df = squared.transform(base_df_snowpark).dataframe
    try:
        assert_dataframe_equal(expected_snow_df, result_df)
    except AssertionError as e:
        assert False, e
