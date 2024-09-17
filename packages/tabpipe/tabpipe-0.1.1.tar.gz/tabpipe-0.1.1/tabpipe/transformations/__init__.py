"""This module contains the transformations classes for tabpipe.

All transformations classes should inherit from the DataProcessing class.

tabpipe already provides a set of transformations classes that can be used to create
ComputedFeatures and can be imported from this module.

Alternatively, you can create your own transformations classes by inheriting from the
DataProcessing class and implementing their logic for the several platforms where
you plan to run them.
"""

from tabpipe.transformations.haversine import Haversine
from tabpipe.transformations.list_categorical import ListCategorical
from tabpipe.transformations.passthrough import PassThrough
from tabpipe.transformations.squared import Squared
from tabpipe.transformations.timestamp_parts import TimestampParts
from tabpipe.transformations.transformation import Transformation
