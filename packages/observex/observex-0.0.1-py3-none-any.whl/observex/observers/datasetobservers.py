"""
This module provides the base class for dataset-specific validation rules
within the ObserveX framework.

The `ObserveXDatasetRuleBase` class is designed to serve as a foundation for implementing custom 
dataset validation logic. It is intended to be subclassed, with subclasses providing the 
specific validation rules to be applied to datasets.
"""
from pyspark.sql.functions import *
from observex.core import base as oxb, utils as u
from observex.observers import observerbase as ob


class ObserveXDatasetRuleBase(ob.ObserveXRuleBase):
    """
    Base class for dataset-specific validation rules in the ObserveX framework.

    This class is meant to be subclassed to implement specific validation rules 
    for datasets. It provides a structure for defining and managing these rules 
    but does not include any implementation details.

    Attributes:
    - `_rule_applies_to`: A string indicating that the rule applies to "dataset".

    Methods:
    - `__init__()`: Initializes the `ObserveXDatasetRuleBase` class. 
    Sets the `_rule_applies_to` attribute to "dataset".

    - `observation_rule(**kwargs)`: Abstract method that must be implemented in subclasses.
    Defines the dataset validation logic. Raises `NotImplementedError` 
    if not overridden in a subclass.
    """
    def __init__(self):
        """
        Initializes the `ObserveXDatasetRuleBase` class by setting the `_rule_applies_to` 
        attribute to "dataset".
        """
        super().__init__()
        self._rule_applies_to = "dataset"

    def observation_rule(self, **kwargs):
        """
        Abstract method for implementing dataset-specific validation logic.

        This method is intended to be overridden in subclasses to define 
        the actual dataset validation rules. It raises a `NotImplementedError`
        if not implemented in a subclass.

        Parameters:
        - **kwargs: Arbitrary keyword arguments to be used by the subclass implementation.

        Raises:
        - NotImplementedError: If not implemented in the subclass.
        """
        raise NotImplementedError("Not implemented in base-class. Must be implemented in sub-class")
