"""
This module defines the `ObserveXInternalUtils` class, which includes utility methods
for use within the ObserveX library. The class extends `ObserveXGlobalBase` from the
`observex.core.base` module and provides various functionalities such as checking for 
null or empty strings, converting observer names to class names, converting dictionaries 
to Spark DataFrames, and standardizing parameter names.

Additionally, this module imports `SparkSession` from `pyspark.sql` to facilitate
the creation and manipulation of Spark DataFrames.
"""
from pyspark.sql import SparkSession
import observex.core.base as oxb


spark = SparkSession.builder.appName(__package__).getOrCreate()

class ObserveXInternalUtils(oxb.ObserveXGlobalBase):
    """
    Internal utility class for the ObserveX library.

    Inherits from `ObserveXGlobalBase` and provides utility methods for common tasks
    within the ObserveX library. These include checking for null or empty strings,
    converting observer names to class names, converting data to Spark DataFrames, and
    standardizing parameter names.

    Methods:
        __init__(self):
            Initializes the ObserveXInternalUtils class, inheriting from ObserveXGlobalBase.
        
        is_null_or_empty_string(self, val, treat_as_null_values=None):
            Checks if a given value is a null or empty string.

        convert_observer_name_to_class_name(self, name):
            Converts an observer name from snake_case to CamelCase format.

        convert_dict_to_df(self, list_rows_data, headers):
            Converts a list of dictionary data and headers into a Spark DataFrame.

        standardize_parameters(rule_args):
            Standardizes parameter names by mapping variations to common names.
    """
    def __init__(self):
        """
        Initializes the ObserveXInternalUtils class by calling the constructor
        of the base class `ObserveXGlobalBase`.
        """
        super().__init__()

    def is_null_or_empty_string(self, val, treat_as_null_values=None):
        """
        Checks if a given value is a null or empty string.

        Parameters:
            val: The value to check. Can be of any type.
            treat_as_null_values (list of str, optional): A list of additional null values 
            to consider.Defaults to None.

        Returns:
            bool: True if the value is None, an empty string, or in the list of null values. 
            False otherwise.
        
        This method also logs the check process for debugging purposes.
        """
        oxb.logging.debug("Checking for None and blank values")
        r_val = (val is None or not isinstance(val, str) or val.strip() == '')
        if treat_as_null_values is None:
            treat_as_null_values = []
        r_val = r_val or (val.strip().lower() in (s.lower() for s in treat_as_null_values))
        return r_val

    def convert_observer_name_to_class_name(self, name):
        """
        Converts an observer name from snake_case format to CamelCase format.

        Parameters:
            name (str): The observer name in snake_case.

        Returns:
            str: The class name in CamelCase format.
        
        This method also logs the conversion process for debugging purposes.
        """
        oxb.logging.debug(f"Finding class name for {name}")
        nm_arr = name.split('_')
        return nm_arr[0] + ''.join(word.capitalize() for word in nm_arr[1:])

    def convert_dict_to_df(self, list_rows_data, headers):
        """
        Converts a list of dictionary data and headers into a Spark DataFrame.

        Parameters:
            list_rows_data (list of dict): The data to be converted into a DataFrame.
            headers (list of str): The column headers for the DataFrame.

        Returns:
            pyspark.sql.DataFrame: The resulting Spark DataFrame.

        Raises:
            ValueError: If the parameters to create the DataFrame are not valid.

        This method also logs the process of creating the DataFrame for debugging purposes.
        """
        oxb.logging.debug("Getting the rows and headers")
        results_ = spark.createDataFrame(list_rows_data, headers)
        if results_ is not None:
            return results_
        else:
            oxb.logging.error("Parameters to create DataFrame are not valid")
            raise ValueError("Parameters to create DataFrame are not valid")

    @staticmethod
    def standardize_parameters(rule_args):
        """
        Standardizes parameter names by mapping various names to common names.

        Parameters:
            rule_args (dict): A dictionary of rule arguments with potentially 
            varied parameter names.

        Returns:
            dict: A dictionary with standardized parameter names and their corresponding values.

        If the "sev_level" parameter is not provided, it defaults to "error".
        """
        param_map = {
            "min_val": ["minimum_value", "min_value", "minimum_val", "min_val", "min"],
            "max_val": ["maximum_value", "max_value", "maximum_val", "max_val"],
            "min_len": ["minimum_length", "min_length", "minimum_len", "min_len"],
            "max_len": ["maximum_length", "max_length", "maximum_len", "max_len"],
            "threshold": ["threshold_value", "thresh", "limit","threshold"],
            "regex_pattern": ["regex", "pattern", "regex_pattern"],
            "col_name": ["column_name", "columns_name", "column_names","col_name"],
            "sev_level": ["severity_level", "severity", "sev_level"]
        }
        standardized_params = {}
        for key, variations in param_map.items():
            for var in variations:
                if var in rule_args:
                    standardized_params[key] = rule_args[var]
                          
        # Remove old keys from rule_args and update with standardized keys
        for key, variations in param_map.items():
            for var in variations:
                if var in rule_args:
                    del rule_args[var]
        
        # Add the standardized parameters back into the original rule_args
        rule_args.update(standardized_params)

        #Default Severity Level      
        if "sev_level" not in rule_args:
            rule_args["sev_level"] = "error"

        return rule_args


class BaseValidator:
    """
    Abstract base class for parameter validation.

    Defines an interface for validating parameters. Subclasses must implement
    the `validate` method to perform specific validation logic.

    Methods:
        validate(self, value):
            Validates the provided value. Must be implemented by subclasses.
    """
    def validate(self, value):
        """
        Validates the provided value.

        Parameters:
            value: The value to validate.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement the validate method")


class ObservexParameterValidator:
    """
    Class for validating parameters used in the ObserveX library.

    Provides static methods for validating non-empty values and checking data types.

    Methods:
        validate_non_empty(value, name):
            Validates that a value is not None or an empty string.

        validate_type(value, expected_type, name):
            Validates that a value is of the expected type.
    """
    @staticmethod
    def validate_non_empty(value, name):
        """
        Validates that a value is not None or an empty string.

        Parameters:
            value: The value to check.
            name (str): The name of the parameter being checked.

        Raises:
            ValueError: If the value is None or an empty string.
        """
        if value is None or value == '':
            raise ValueError(f"{name} must not be None or empty")

    @staticmethod
    def validate_type(value, expected_type, name):
        """
        Validates that a value is of the expected type.

        Parameters:
            value: The value to check.
            expected_type (type): The expected type of the value.
            name (str): The name of the parameter being checked.

        Raises:
            TypeError: If the value is not of the expected type.
        """
        if not isinstance(value, expected_type):
            raise TypeError(f"{name} must be of type {expected_type}, got {type(value)}")


class RuleValidator:
    """
    Class for validating rules and datasets.

    Provides static methods for checking data types and validating rulesets.

    Methods:
        validate_data_type(dataset, expected_type):
            Validates that a dataset is of the expected type.

        validate_ruleset(ruleset):
            Validates that a ruleset is a list.
    """
    ALLOWED_DATA_TYPES = {"spark_dataframe"}

    @staticmethod
    def validate_data_type(dataset, expected_type):
        """
        Validates that a dataset is of the expected type.

        Parameters:
            dataset: The dataset to check.
            expected_type (type): The expected type of the dataset.

        Raises:
            TypeError: If the dataset is not of the expected type.
        """
        if not isinstance(dataset, expected_type):
            raise TypeError(f"Expected dataset of type {expected_type}, got {type(dataset)}")

    @staticmethod
    def validate_ruleset(ruleset):
        """
        Validates that a ruleset is a list.

        Parameters:
            ruleset: The ruleset to check.

        Raises:
            TypeError: If the ruleset is not a list.
        """
        if not isinstance(ruleset, list):
            raise TypeError("Ruleset must be a list")
