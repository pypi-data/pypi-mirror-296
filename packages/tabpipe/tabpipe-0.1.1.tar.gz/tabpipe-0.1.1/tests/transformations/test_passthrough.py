from pandas.testing import assert_frame_equal
from snowflake.snowpark.testing import assert_dataframe_equal

from tabpipe.dataframe import DataFrame


def test_passthrough_transform_pandas(
    base_df, passthrough_transformation, passthrough_expected_df
):
    """Test the transform_pandas method of the Passthrough operation."""
    result_df = passthrough_transformation.transform(base_df).dataframe

    assert (
        assert_frame_equal(passthrough_expected_df, result_df, check_like=True) is None
    )


def test_passthrough_transform_snowpark(
    snowflake_connection,
    base_df_snowpark,
    passthrough_transformation,
    passthrough_expected_df,
):
    """Test the transform_snowpark method of the Squared operation."""
    expected_snow_df = snowflake_connection.create_dataframe(passthrough_expected_df)

    result_df = (
        passthrough_transformation.transform(base_df_snowpark).sort_columns().dataframe
    )

    expected_snow_df = DataFrame.from_object(expected_snow_df).sort_columns().dataframe

    try:
        assert_dataframe_equal(expected_snow_df, result_df)
    except AssertionError as e:
        assert False, e
