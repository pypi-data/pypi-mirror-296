"""
This module defines classes and functions for implementing and managing observation rules 
within the ObserveX library. It focuses on the validation and application of rules to 
metadata, extending the base functionality provided by the `observex.core` and `observex.observers` 
modules.

"""
from pyspark.sql.functions import *
from observex.core import base as oxb, utils as u
from observex.observers import observerbase as ob


class ObserveXMetadataRuleBase(ob.ObserveXRuleBase):
    """
    Base class for metadata validation rules in ObserveX.

    This class is intended to be a base for implementing metadata validation rules within the 
    ObserveX framework. It inherits from `ObserveXRuleBase` and sets up the foundation for 
    applying rules to metadata.

    Attributes:
    - _rule_applies_to (str): Specifies that the rule applies to "metadata".

    Methods:
    - __init__(): Initializes the base class and sets the rule applicability to metadata.
    - observation_rule(**kwargs): Placeholder method to be implemented in subclasses.
    """
    def __init__(self):
        """
        Initializes the `ObserveXMetadataRuleBase` instance.

        This constructor sets the `_rule_applies_to` attribute to "metadata", indicating that 
        the rules derived from this base class are meant for metadata validation.
        """
        super().__init__()
        self._rule_applies_to = "metadata"

    def observation_rule(self, **kwargs):
        """
        Defines the observation rule to be applied.

        This method is intended to be overridden by subclasses to implement specific metadata 
        validation logic. As it stands, it raises a `NotImplementedError` to signal that it 
        must be implemented in derived classes.

        Parameters:
        - **kwargs: Arbitrary keyword arguments that may be required for the rule implementation.

        Raises:
        - NotImplementedError: If called directly from this base class, indicating that it must 
          be implemented in a subclass.
        """
        raise NotImplementedError("Not implemented in base-class. Must be implemented in sub-class")
