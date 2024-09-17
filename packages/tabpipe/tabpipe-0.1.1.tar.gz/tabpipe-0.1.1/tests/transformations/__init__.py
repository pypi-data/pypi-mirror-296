"""Unit test package for tabpipe.transformations module.

Tabpipe relies on the Transformation abstract class to define the base behavior
of data transformations. So out testing approach will be to:
- For each class that inherits from Transformation, we will create a test file where we will test:
    - Instantiating the class
    - The `transform_*` methods for the supported data platforms (e.g. pandas, snowpark)
        (using fit_transform underneath when the transformation needs to be fitted)
    - Any other features that may be specific to the transformation
- In `test_transformation.py`, we test any methods that are common to all transformations
and that are not already covered by the tests for the subclasses.
"""
