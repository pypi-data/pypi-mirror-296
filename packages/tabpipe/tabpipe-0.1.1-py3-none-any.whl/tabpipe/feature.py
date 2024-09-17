from typing import Type

from tabpipe.data_types import DataType


class Feature:
    """A column in a dataframe that can be used for analysis.

    This classes defines the basic behavior of a feature.
    """

    def __init__(
        self,
        name: str,
        description: str,
        data_type: Type[DataType],
    ):
        """Initialize a feature.

        Args:
            name: The name of the feature.
            description: A description of the feature.
            data_type: The data type of the feature.
        """
        self._name: str = name
        self._description: str = description
        self._data_type: Type[DataType] = data_type

    @property
    def name(self) -> str:
        """The name of the feature.

        Returns:
            The name of the feature.
        """
        return self._name

    @property
    def description(self) -> str:
        """A description of the feature.

        Returns:
            The description of the feature.
        """
        return self._description

    @property
    def data_type(self) -> Type[DataType]:
        """The data type of the feature.

        Returns:
            The data type of the feature.
        """
        return self._data_type
