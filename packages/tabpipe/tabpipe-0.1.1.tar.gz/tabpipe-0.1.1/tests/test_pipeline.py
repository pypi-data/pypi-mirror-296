import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from snowflake.snowpark.testing import assert_dataframe_equal

from tabpipe.data_types import NumericDataType
from tabpipe.exceptions import DuplicateFeature, DuplicateTransformation, NotFittedError
from tabpipe.pipeline import Pipeline
from tabpipe.transformations import PassThrough, TimestampParts
from tabpipe.units import DateTimeParts

# TODO: Tests for the Pipeline class


def test_raises_value_error_if_pipeline_not_fit_before_getting_output_features(
    pipeline_1,
):
    """Test that a ValueError is raised if the pipeline is not fit before getting output features."""
    with pytest.raises(
        ValueError, match="Pipeline must be fit before output features can be retrieved"
    ):
        _ = pipeline_1.output_features


def test_raises_value_error_if_pipeline_not_fit_before_transforming_data(pipeline_1):
    """Test that a ValueError is raised if the pipeline is not fit before transforming data."""
    with pytest.raises(NotFittedError):
        pipeline_1.transform(pd.DataFrame())


def test_raises_duplicate_feature_error_if_feature_with_same_name_added():
    """Test that a DuplicateFeature error is raised if a feature with the same name is added to the pipeline."""
    with pytest.raises(
        DuplicateFeature,
    ):
        Pipeline(
            [
                TimestampParts(["input"], output_parts=[DateTimeParts.DAY]),
                PassThrough(["input2"], name="TimestampParts(input).day"),
            ]
        )


def test_raises_duplicate_transformation_error_if_transformation_with_same_name_added():
    """Test that a DuplicateTransformation error is raised if a transformation with the same name is added to the pipeline."""
    with pytest.raises(
        DuplicateTransformation,
    ):
        Pipeline(
            [
                PassThrough(["input1"], name="transformation"),
                PassThrough(["input2"], name="transformation"),
            ]
        )


def test_fit_transform_pandas(
    pipeline_1, base_df, expected_transformed_base_df_pipeline_1_pandas
):
    """Test the fit_transform method of the Pipeline class for pandas dataframes."""
    result_df = pipeline_1.fit_transform(base_df)
    assert (
        assert_frame_equal(
            expected_transformed_base_df_pipeline_1_pandas, result_df, check_like=True
        )
        is None
    )


def test_fit_transform_snowpark(
    pipeline_1, base_df_snowpark, expected_transformed_base_df_pipeline_1_snowpark
):
    """Test the fit_transform method of the Pipeline class for Snowpark dataframes."""
    result_df = pipeline_1.fit_transform(base_df_snowpark)
    try:
        assert_dataframe_equal(
            expected_transformed_base_df_pipeline_1_snowpark, result_df
        )
    except AssertionError as e:
        assert False, e


def test_transform_pandas(
    fitted_pipeline_1, base_df, expected_transformed_base_df_pipeline_1_pandas
):
    """Test the fit_transform method of the Pipeline class for pandas dataframes."""
    result_df = fitted_pipeline_1.transform(base_df)
    assert (
        assert_frame_equal(
            expected_transformed_base_df_pipeline_1_pandas, result_df, check_like=True
        )
        is None
    )


def test_transform_snowpark(
    fitted_pipeline_1,
    base_df_snowpark,
    expected_transformed_base_df_pipeline_1_snowpark,
):
    """Test the fit_transform method of the Pipeline class for Snowpark dataframes."""
    result_df = fitted_pipeline_1.transform(base_df_snowpark)
    try:
        assert_dataframe_equal(
            expected_transformed_base_df_pipeline_1_snowpark, result_df
        )
    except AssertionError as e:
        assert False, e


def initializes_pipeline_correctly_with_valid_transformations(pipeline_1):
    """Test that the Pipeline class initializes correctly with valid transformations."""
    assert all(
        name in pipeline_1.transformations
        for name in [
            "Input(a)",
            "Squared(a)",
            "Haversine",
            "ListCategorical(fruits)",
            "TimestampParts(timestamp_1)",
            "input_squared",
            "squared_squared",
        ]
    )


def raises_value_error_if_pipeline_not_fit_before_getting_filtered_output_features():
    """Test that a ValueError is raised if the pipeline is not fit before getting filtered output features."""
    with pytest.raises(
        ValueError, match="Pipeline must be fit before output features can be retrieved"
    ):
        Pipeline([]).filtered_output_features(lambda f: True)


def test_output_features(
    pipeline_1, base_df, expected_transformed_base_df_pipeline_1_pandas
):
    """Test the output_features method of the Pipeline class."""
    with pytest.raises(
        ValueError, match="Pipeline must be fit before output features can be retrieved"
    ):
        pipeline_1.output_features

    pipeline_1.fit(base_df)

    assert all(
        f in expected_transformed_base_df_pipeline_1_pandas.columns
        for f in pipeline_1.output_features
    )


def test_filtered_output_features(
    pipeline_1, base_df, expected_transformed_base_df_pipeline_1_pandas
):
    """Test the filtered_output_features method of the Pipeline class."""
    with pytest.raises(
        ValueError, match="Pipeline must be fit before output features can be retrieved"
    ):
        pipeline_1.filtered_output_features(lambda f: True)

    pipeline_1.fit(base_df)

    assert set(pipeline_1.filtered_output_features(lambda f: "squared" in f.name)) == {
        "a_squared",
        "passthrough_squared",
        "squared_squared",
    }

    assert all(
        f.name
        in [
            "a",
            "Squared(a)",
            "Haversine",
            "TimestampParts(timestamp_1).year",
            "TimestampParts(timestamp_1).month",
            "TimestampParts(timestamp_1).day",
            "TimestampParts(timestamp_1).hour",
            "TimestampParts(timestamp_1).minute",
            "TimestampParts(timestamp_1).second",
            "TimestampParts(timestamp_1).day_of_week",
            "a_squared",
            "passthrough_squared",
            "squared_squared",
        ]
        for f in pipeline_1.filtered_output_features(
            lambda f: issubclass(f.data_type, NumericDataType), return_object=True
        )
    )
