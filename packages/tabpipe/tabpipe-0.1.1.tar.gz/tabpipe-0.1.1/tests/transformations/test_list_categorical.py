from pandas.testing import assert_frame_equal
from snowflake.snowpark.testing import assert_dataframe_equal


def test_list_categorical_transform_pandas1(
    base_list_categorical_df, expected_list_categorical_df1, list_categorical_1
):
    """Test the transform_pandas method of the ListCategorical operation."""
    result_df = list_categorical_1.fit_transform(base_list_categorical_df).dataframe
    assert (
        assert_frame_equal(expected_list_categorical_df1, result_df, check_like=True)
        is None
    )


def test_list_categorical_transform_pandas2(
    base_list_categorical_df, expected_list_categorical_df2, list_categorical_2
):
    """Test the transform_pandas method of the ListCategorical operation."""
    result_df = list_categorical_2.fit_transform(base_list_categorical_df).dataframe
    assert (
        assert_frame_equal(expected_list_categorical_df2, result_df, check_like=True)
        is None
    )


def test_list_categorical_transform_snowpark1(
    snowflake_connection,
    base_list_categorical_snowpark_df,
    list_categorical_1,
    expected_list_categorical_df1,
):
    """Test the transform_snowpark method of the ListCategorical operation."""
    expected_snow_df = snowflake_connection.create_dataframe(
        expected_list_categorical_df1
    )

    result_df = list_categorical_1.fit_transform(
        base_list_categorical_snowpark_df
    ).dataframe
    try:
        assert_dataframe_equal(expected_snow_df, result_df)
    except AssertionError as e:
        assert False, e


def test_list_categorical_transform_snowpark2(
    snowflake_connection,
    base_list_categorical_snowpark_df,
    list_categorical_2,
    expected_list_categorical_df2,
):
    """Test the transform_snowpark method of the Squared operation."""
    expected_snow_df = snowflake_connection.create_dataframe(
        expected_list_categorical_df2
    )

    result_df = list_categorical_2.fit_transform(
        base_list_categorical_snowpark_df
    ).dataframe
    try:
        assert_dataframe_equal(expected_snow_df, result_df)
    except AssertionError as e:
        assert False, e
