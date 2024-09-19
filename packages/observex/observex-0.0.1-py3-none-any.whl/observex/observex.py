"""
This module provides the `ObserveX` class, which serves as the main entry point for executing 
observation rules within the ObserveX library.

The `ObserveX` class includes methods to observe and scan datasets based on a set of rules. 
It acts as a wrapper to initialize and validate parameters before passing them to the 
`ObserveXExecutor` for execution.
"""
import logging
from pyspark.sql import DataFrame
from observex.executors.oxexecutors import ObserveXExecutor
from observex.core.exceptions import *
from observex.core.base import ObserveXGlobalBase as oxb
from observex.core.utils import *
from observex.observers.rowobservers import ObserveXRowRuleFactory
from observex.observers.columnobservers import ObserveXColumnRuleFactory

class ObserveX:
    """
    Main class for managing and executing observation rules within the ObserveX library.

    This class provides static methods to observe and scan datasets using specified rules. 
    It validates input parameters and delegates execution to the `ObserveXExecutor`.

    Attributes:
    - custom_validators (list): A list of custom validators to be applied to the dataset.

    Methods:
    - add_custom_validator(validator): Adds a custom validator to the list of validators.
    - observe(dataset, ruleset, logging_level='INFO', separate_columns=False): 
    Observes the dataset based on the provided ruleset.
    - scan(dataset, ruleset, logging_level='INFO', separate_columns=False): 
    Scans the dataset using the same method as `observe`.
    - _observe(dataset, ruleset, separate_columns): Validates parameters and 
    passes them to the `ObserveXExecutor` for execution.
    """
    custom_validators = []

    @staticmethod
    def add_custom_validator(validator):
        """
        Adds a custom validator to the list of validators.

        This method allows users to register custom validation logic to be applied to the dataset 
        before executing observation rules.

        Parameters:
        - validator (BaseValidator): An instance of a custom validator that extends `BaseValidator`.

        Raises:
        - TypeError: If the provided validator is not an instance of `BaseValidator`.
        """
        if not isinstance(validator, BaseValidator):
            raise TypeError("Custom validator must be an instance of BaseValidator")
        ObserveX.custom_validators.append(validator)

    @staticmethod
    def observe(dataset, ruleset, logging_level='INFO', separate_columns=False):
        """
        Observes the dataset based on the provided ruleset.

        This method serves as an entry point to start the observation process. It validates the 
        parameters and then delegates the execution to the `_observe` method.

        Parameters:
        - dataset (Spark DataFrame): The dataset to be observed.
        - ruleset (list of dict): The list of rules to apply to the dataset.
        - logging_level (str): The logging level to be set for the observation process.
        - separate_columns (bool): Whether to separate validation information into distinct columns. 
        Defaults to False.

        Returns:
        - The result of the observation execution, which is obtained from the `ObserveXExecutor`.

        Raises:
        - ValueError: If the dataset or ruleset parameters are None.
        """
        logging.basicConfig(level=getattr(logging, logging_level.upper(), 'INFO'))

        try:
            ObservexParameterValidator.validate_type(dataset, DataFrame, "Dataset")
            ObservexParameterValidator.validate_type(ruleset, list, "Ruleset")

            
            for validator in ObserveX.custom_validators:
                validator.validate(dataset)
        except ValueError as e:
            logging.error(f"Parameter validation failed: {e}")  # Replace oxb.logging with logging
            raise

        return ObserveX._observe(dataset, ruleset, separate_columns)

    @staticmethod
    def scan(dataset, ruleset, logging_level='INFO', separate_columns=False):
        """
        Scans the dataset based on the provided ruleset.

        This method is an alias for `observe` and provides the same functionality for observing 
        datasets. It validates the parameters and delegates the execution to the `_observe` method.

        Parameters:
        - dataset (Spark DataFrame): The dataset to be scanned.
        - ruleset (list of dict): The list of rules to apply to the dataset.
        - logging_level (str): The logging level to be set for the scan process. Defaults to 'INFO'.
        - separate_columns (bool): Whether to separate validation information into distinct columns. 
        Defaults to False.

        Returns:
        - The result of the observation execution, which is obtained from the `ObserveXExecutor`.

        Raises:
        - ValueError: If the dataset or ruleset parameters are None.
        """
        return ObserveX.observe(dataset, ruleset, logging_level, separate_columns)
    
    @staticmethod
    def observe_with_rules(dataset, ruleset, logging_level='INFO'):
        logging.basicConfig(level=getattr(logging, logging_level.upper(), 'INFO'))

        try:
            RuleValidator.validate_data_type(dataset, "spark_dataframe")  
            RuleValidator.validate_ruleset(ruleset)

            # Apply custom validators
            for validator in ObserveX.custom_validators:
                validator.validate(dataset)

        except (TypeError, ValueError) as e:
            logging.error(f"Validation failed: {e}")
            raise

        return ObserveX._observe(dataset, ruleset)


    @staticmethod
    def scan_with_rules(dataset, ruleset, logging_level='INFO'):
        return ObserveX.observe_with_rules(dataset, ruleset, logging_level)

    @staticmethod
    def _observe(dataset, ruleset, separate_columns):
        """
        Validates the parameters and passes them to the `ObserveXExecutor` for execution.

        This method performs parameter validation and handles logging. It then calls the 
        `ObserveXExecutor` to execute the observation rules on the dataset.

        Parameters:
        - dataset (Spark DataFrame): The dataset to be observed.
        - ruleset (list of dict): The list of rules to apply to the dataset.
        - separate_columns (bool): Whether to separate validation information into distinct columns.

        Returns:
        - The result of the observation execution from the `ObserveXExecutor`.

        Raises:
        - ValueError: If the dataset or ruleset parameters are None.
        """
        oxb.logging.debug("Validating the Parameters")

        # Check if dataset and ruleset are valid
        if dataset is None:
            logging.error("Invalid values passed for parameters dataset: None")  # Replace oxb.logging with logging
            raise ValueError("Invalid values passed for parameters dataset: None")
        if ruleset is None:
            oxb.logging.error("Invalid values passed for parameters ruleset: None")
            raise ValueError("Invalid values passed for parameters ruleset: None")

        # Standardize parameters for each rule in the ruleset
        standardized_ruleset = []
        for rule in ruleset:
            standardized_rule = ObserveXInternalUtils.standardize_parameters(rule)
            rule_name = standardized_rule.get("observe", "")
            rule_type = standardized_rule.get("rule_type", "").lower()

            if "row" in rule_type:
                logging.debug(f"Using Row Observer Factory for rule: {rule_name}")
                factory = ObserveXRowRuleFactory()
            elif "column" in rule_type:
                logging.debug(f"Using Column Observer Factory for rule: {rule_name}")
                factory = ObserveXColumnRuleFactory()
            else:
                raise ValueError(f"Unknown or missing 'rule_type' for rule: {standardized_rule}")

            standardized_rule["observe"] = factory._normalize_class_name(rule_name)
            standardized_ruleset.append(standardized_rule)

        # Pass the standardized ruleset and separate_columns to the executor
        oxb.logging.debug("Executing the ObserveXExecutor with standardized dataset, ruleset, and separate_columns=%s", separate_columns)
        result = ObserveXExecutor().execute(dataset, standardized_ruleset, separate_columns)
        if  result is not None and len(result)>0:
            return result
        else:
            oxb.logging.error("Unable to get the result error at oxexecutors for the ruleset", separate_columns)
            