from graphlib import TopologicalSorter
from typing import Any, Callable, Dict, Iterable, List, Union

from tabpipe.dataframe import DataFrame
from tabpipe.exceptions import DuplicateFeature, DuplicateTransformation, NotFittedError
from tabpipe.feature import Feature
from tabpipe.transformations import PassThrough, Transformation


class Pipeline:
    """A collection of features that can be used to transform data.

    These features probably have dependencies between them that can be represented as a
    Directed Acyclic Graph (DAG).

    This class is the main entry point for interacting with the library. In a typical
    use case, you would create a pipeline with a set of features, fit the pipeline to
    some data, and then save it as an artifact so that it can later be used to
    transform new data (potentially in a different environment).
    """

    def __init__(self, transformations: Iterable[Transformation]):
        """Initialize a pipeline.

        Args:
            transformations: The features that compose the pipeline.

        Raises:
            DuplicateFeature: If a feature with the same name already exists in the
                dataset.
            ValueError: If the id column is not an InputFeature.
        """
        self._transformations: Dict[str, Transformation] = {}
        self._features: Dict[str, Feature] = {}
        self._source_transformation: Dict[str, str] = {}
        self._transformation_dag: Dict[str, List[str]] = {}
        self._is_fit: bool = False

        for t in transformations:
            self._add_transformation(t)

        self._build_dag()

        # Check if DAG is valid
        TopologicalSorter(self._transformation_dag).prepare()

    @property
    def is_fit(self) -> bool:
        """Whether the pipeline has been fit to data.

        Returns:
            Whether the pipeline has been fit to data.
        """
        return self._is_fit

    @property
    def transformations(self) -> Dict[str, Transformation]:
        """The transformations in the pipeline.

        Returns:
            The transformations in the pipeline.
        """
        return self._transformations

    @property
    def output_features(self) -> List[str]:
        """The names of the output features of the pipeline.

        Returns:
            The names of the output features of the pipeline.
        """
        feature_names = [
            # I have to do this because linter doesn't
            # understand the return_object parameter
            f.name if isinstance(f, Feature) else f
            for f in self.filtered_output_features(lambda _: True, return_object=False)
        ]

        return feature_names

    @property
    def dag(self) -> Dict[str, List[str]]:
        """Directed Acyclic Graph (DAG) with the pipeline's features.

        Returns:
            The Directed Acyclic Graph (DAG) of the pipeline.
        """
        return self._transformation_dag

    def filtered_output_features(
        self, filter_func: Callable[[Feature], bool], return_object: bool = False
    ) -> List[Union[str, Feature]]:
        """Get the output features of the pipeline.

        This function can be useful when one wants to retrieve only a subset of the
        output features of the pipeline (e.g., only the features that are of a certain
        type).

        Args:
            filter_func: The function to filter the features.
            return_object: Whether to return the feature object or the feature name.

        Returns:
            The output features of the pipeline.
        """
        if not self._is_fit:
            raise ValueError(
                "Pipeline must be fit before output features can be retrieved"
            )

        return [
            f if return_object else name
            for name, f in self._features.items()
            if filter_func(f)
        ]

    def _add_feature(self, feature: Feature, source_transformation: str) -> None:
        """Add a feature to the pipeline.

        This method should be used when:
        - a transformation is added to the pipeline and its output is already known
        - a transformation is fitted and its output becomes known

        Args:
            feature: The feature to add to the pipeline.
            source_transformation: The name of the transformation that produces the feature.

        Raises:
            DuplicateFeature: If a feature with the same name already exists in the
                dataset.
        """
        if feature.name in self._features:
            raise DuplicateFeature(
                f"Feature with name '{feature.name}' already produced by Transformation with name '{self._source_transformation[feature.name]}'"
            )

        self._features[feature.name] = feature
        self._source_transformation[feature.name] = source_transformation

    def _add_transformation(self, transformation: Transformation) -> None:
        """Add a feature to the pipeline.

        This method should be used when a transformation is added to the pipeline,
        which only happens when the pipeline is initialized.

        Args:
            transformation: The feature to add to the pipeline.

        Raises:
            DuplicateTransformation: If a transformation with the same name already exists.
        """
        if transformation.name in self._transformations:
            raise DuplicateTransformation(
                f"Transformation with name '{transformation.name}' already exists in the pipeline"
            )

        self._transformations[transformation.name] = transformation

        if transformation.has_known_output:
            for feature in transformation.output:
                self._add_feature(feature, transformation.name)

    def _build_dag(self) -> None:
        """Build the Directed Acyclic Graph (DAG) of the pipeline.

        This method should be called after all transformations have been added to the
        pipeline (when the pipeline is initialized). The DAG is built by resolving the
        dependencies between the transformations based on their input fields:
        - If the input is a Feature, the dependency is the transformation that produces
            the feature. If no transformation produces the feature, then there is no
            dependency, and we assume a column with the name of the input feature exists
            in the dataframe by the time the transformation is applied.
        - If the input is a Transformation, the dependency is the transformation itself.

        Raises:
            ValueError: If a transformation has bad input types.
        """
        for transformation in self._transformations.values():

            dependencies = []
            if not isinstance(transformation, PassThrough):
                for i, it in zip(transformation.input, transformation.input_types):
                    if it == Feature:
                        input_transformation = self._source_transformation.get(i, None)
                    elif it == Transformation:
                        input_transformation = i
                    else:
                        raise ValueError(f"Unsupported input type: {it}")

                    if input_transformation:
                        dependencies.append(input_transformation)

            self._transformation_dag[transformation.name] = dependencies

    def _resolve_inputs(self, transformation: Transformation) -> None:
        """Resolve the inputs of a transformation.

        This method should be called when a transformation is about to be processed.
        It resolves the inputs of the transformation based on the output of its
        dependencies.

        Args:
            transformation: The transformation to resolve the inputs

        Raises:
            ValueError: If the transformation has bad input types.
        """
        new_inputs: List[str] = []
        for i, it in zip(transformation.input, transformation.input_types):
            if it == Transformation:
                new_inputs.extend(out.name for out in self._transformations[i].output)
            elif it == Feature:
                new_inputs.append(i)
            else:
                raise ValueError(f"Unsupported input type: {it}")

        transformation.input = new_inputs

    def _process(self, data: DataFrame, fit: bool = False) -> DataFrame:
        """Process the data using the DAG to know the order of the features to process.

        This method implements a pass through the DAG to process the data. It is used
        both by the fit and transform methods.

        Args:
            data: The data to process.
            fit: Whether to fit the pipeline to the data.
        """
        for t_name in TopologicalSorter(self._transformation_dag).static_order():
            t = self._transformations[t_name]

            # If transformation inputs need to be resolved, we do it here
            if not t.resolved_input_types:
                self._resolve_inputs(t)

            # Transform the data and store the results in the dataframe
            if fit:
                data = t.fit_transform(data)

                # For transformations that need to be fit, we add the output features to the pipeline
                if not t.has_known_output:
                    for f in t.output:
                        self._add_feature(f, t_name)
                    t.has_known_output = True
            else:
                data = t.transform(data)

        if fit:
            self._is_fit = True

        return data.filter_columns(self.output_features)

    def transform(self, data: object) -> object:
        """Transform the data using the pipeline.

        Args:
            data: The data to transform.

        Returns:
            The transformed data.

        Raises:
            ValueError: If the pipeline has not been fit.
        """
        if not self._is_fit:
            raise NotFittedError(self)

        return self._process(DataFrame.from_object(data), fit=False).dataframe

    def fit(self, data: Any) -> None:
        """Fit the pipeline to the data.

        Args:
            data: The data to fit the pipeline to.
        """
        self._process(DataFrame.from_object(data), fit=True)

    def fit_transform(self, data: Any) -> Any:
        """Fit the pipeline to the data and transform it.

        Args:
            data: The data to fit the pipeline to and transform.

        Returns:
            The transformed data.
        """
        return self._process(DataFrame.from_object(data), fit=True).dataframe
