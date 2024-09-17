import pytest

from tabpipe.data_types import BoolDataType, FloatDataType, FloatOrString, IntDataType


def test_data_type(
    passthrough_transformation,
    squared,
    timestamp_parts_1,
    base_timestamps_df,
    list_categorical_1,
    base_list_categorical_df,
):
    """Test the data_type property."""
    assert passthrough_transformation.data_type == [FloatOrString]
    assert squared.data_type == [FloatDataType]
    assert timestamp_parts_1.data_type == [IntDataType] * 7

    with pytest.raises(ValueError):
        _ = list_categorical_1.data_type

    list_categorical_1.fit(base_list_categorical_df)

    assert list_categorical_1.data_type == [BoolDataType] * 3


def test_input_types(
    passthrough_transformation,
    squared,
):
    """Test the input_types property."""
    pass  # TODO


def test_set_input_types():
    pass  # TODO


def test_resolved_input_types():
    pass  # TODO


def test_has_known_outputs():
    pass  # TODO


def test_set_has_known_output():
    pass  # TODO


def test_input():
    pass  # TODO


def test_set_input():
    """Test the set_input method."""
    pass  # TODO


def test_name():
    """Test the name property."""
    pass  # TODO


def test_set_name():
    """Test the set_name method."""
    pass  # TODO


def test_output():
    """Test the output property."""
    pass  # TODO


def test_transform_raise_unsupported_type():
    """Test that the transform method raises an exception when an unsupported dataframe type is provided."""
    pass  # TODO
