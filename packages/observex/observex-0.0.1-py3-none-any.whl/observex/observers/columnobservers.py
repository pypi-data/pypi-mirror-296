from observex.core import base as oxb, utils as u
from observex.observers import observerbase as ob
from pyspark.sql.functions import *
import re
"""
"""

class ObserveXColumnRuleFactory(oxb.ObserveXGlobalBase):
    def __init__(self):
        super().__init__()
    
    def get_instance(self, name):
        """
        This method dynamically finds and returns the column rule class based on the name provided.
        It normalizes the class name by handling variations like underscores, hyphens, and different cases.
        """
        # Normalize the class name
        normalized_name = self._normalize_class_name(name)

        # Try to find a class in globals() with the same name, ignoring case
        for class_name in globals():
            if class_name.lower() == normalized_name.lower():
                obj = globals()[class_name]
                if issubclass(obj, ObserveXColumnRuleBase):  # This is now specific to column rules
                    return obj()
                else:
                    raise NotImplementedError(f"[{name}] is not found OR is not implemented as a column rule.")

        raise NameError(f"[{normalized_name}] is not found OR is not implemented in global context as a column rule.")

    def _normalize_class_name(self, name):
        """
        Normalize the column rule class name by handling different variations dynamically.
        E.g., 'FieldValueBetween', 'field_value_between', etc.
        """
        # Remove any 'Observe' prefix if present
        name = name.replace('Observe', '').strip()

        # Split the name by underscores, hyphens, or spaces
        name_parts = re.split(r'[_\s-]', name)

        # Capitalize the first letter of each part without altering the rest
        normalized_name = ''.join([part[:1].upper() + part[1:] if part else '' for part in name_parts])
        
        # Add 'Observe' prefix back and return the normalized class name
        return f"Observe{normalized_name}"
    

class ObserveXColumnRuleBase(ob.ObserveXRuleBase):
    """
    """
    def __init__(self):
        super().__init__()
        self._rule_applies_to = "column"

    def observation_rule(self, **kwargs):
        raise NotImplementedError("Not implemented in base-class. Must be implemented in sub-class")
    
    def _get_rule_col_name(self, col_name):
        return f"__ox_{col_name}_{type(self).__name__}__"
    

class ObserveColumnMaxString(ObserveXColumnRuleBase):
    """
    A rule to observe the maximum string length of a specified column.
    Inherits from ObserveXColumnRuleBase. Defines a rule for calculating the maximum length of strings in a given column.
    """
    
    def __init__(self):
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Defines the rule for the maximum string length of a column.
        Args:
            **kwargs: Must include 'col_name' for the column.
        Returns:
            tuple: (scope, {'rule_col_name': col_name, 'rule_def': rule_def})
        Raises:
            ValueError: If 'col_name' is missing.
        """
        col_name = kwargs.get('col_name', None)

        if col_name is None:
            raise ValueError("Invalid or missing column name")

        rule_def = f"MAX(LENGTH({col_name}))"

        return_val = {
            "rule_col_name": col_name,
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val


class ObserveColumnMinString(ObserveXColumnRuleBase):
    """
    A rule to observe the minimum string length of a specified column.

    Inherits from ObserveXColumnRuleBase. Defines a rule for calculating the minimum length of strings in a given column.
    """
    def __init__(self):
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Defines the rule for the minimum string length of a column.
        Args:
            **kwargs: Must include 'col_name' for the column.
        Returns:
            tuple: (scope, {'rule_col_name': col_name, 'rule_def': rule_def})
        Raises:
            ValueError: If 'col_name' is missing.
        """
        col_name = kwargs.get('col_name', None)

        if col_name is None:
            raise ValueError("Invalid or missing column name")

        rule_def = f"MIN(LENGTH({col_name}))"

        return_val = {
            "rule_col_name": col_name,
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val


class ObserveColumnAvgString(ObserveXColumnRuleBase):
    """
    A rule to observe the average string length of a specified column.

    Inherits from ObserveXColumnRuleBase. Defines a rule for calculating the average length of strings in a given column.
    """
    def __init__(self):
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Defines the rule for the average string length of a column.
        Args:
            **kwargs: Must include 'col_name' for the column.
        Returns:
            tuple: (scope, {'rule_col_name': col_name, 'rule_def': rule_def})
        Raises:
            ValueError: If 'col_name' is missing.
        """
        col_name = kwargs.get('col_name', None)

        if col_name is None:
            raise ValueError("Invalid or missing column name")

        rule_def = f"AVG(LENGTH({col_name}))"

        return_val = {
            "rule_col_name": col_name,
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val


class ObserveColumnNullCount(ObserveXColumnRuleBase):
    """
    A rule to observe the count of null values in a specified column.

    Inherits from ObserveXColumnRuleBase. Defines a rule for calculating the total number of null values in a given column.
    """
    def __init__(self):
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Defines the rule for counting null values in a column.
        Args:
            **kwargs: Must include 'col_name' for the column.
        Returns:
            tuple: (scope, {'rule_col_name': col_name, 'rule_def': rule_def})
        Raises:
            ValueError: If 'col_name' is missing.
        """
        col_name = kwargs.get('col_name', None)

        if col_name is None:
            raise ValueError("Invalid or missing column name")

        rule_def = f"SUM(CASE WHEN {col_name} IS NULL THEN 1 ELSE 0 END)"

        return_val = {
            "rule_col_name": col_name,
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val


class ObserveColumnPercentNullCount(ObserveXColumnRuleBase):
    """
    A rule to observe the percentage of null values in a specified column.

    Inherits from ObserveXColumnRuleBase. Defines a rule for calculating the percentage of null values in a given column.
    """
    def __init__(self):
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Defines the rule for calculating the percentage of null values in a column.
        Args:
            **kwargs: Must include 'col_name' for the column.
        Returns:
            tuple: (scope, {'rule_col_name': col_name, 'rule_def': rule_def})
        Raises:
            ValueError: If 'col_name' is missing.
        """
        col_name = kwargs.get('col_name', None)

        if col_name is None:
            raise ValueError("Invalid or missing column name")

        rule_def = f"(SUM(CASE WHEN {col_name} IS NULL THEN 1 ELSE 0 END) / COUNT(*)) * 100"

        return_val = {
            "rule_col_name": col_name,
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val


class ObserveColumnEmptyStringCount(ObserveXColumnRuleBase):
    """
    A rule to observe the count of empty strings in a specified column.

    Inherits from ObserveXColumnRuleBase. Defines a rule for calculating the total number of empty strings in a given column.
    """
    def __init__(self):
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Defines the rule for counting empty strings in a column.
        Args:
            **kwargs: Must include 'col_name' for the column.
        Returns:
            tuple: (scope, {'rule_col_name': col_name, 'rule_def': rule_def})
        Raises:
            ValueError: If 'col_name' is missing.
        """
        col_name = kwargs.get('col_name', None)

        if col_name is None:
            raise ValueError("Invalid or missing column name")

        rule_def = f"SUM(CASE WHEN {col_name} = '' THEN 1 ELSE 0 END)"

        return_val = {
            "rule_col_name": col_name,
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val


class ObserveColumnPercentEmptyStringCount(ObserveXColumnRuleBase):
    """
    A rule to observe the percentage of empty strings in a specified column.

    Inherits from ObserveXColumnRuleBase. Defines a rule for calculating the percentage of empty strings in a given column.
    """
    def __init__(self):
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Defines the rule for calculating the percentage of empty strings in a column.
        Args:
            **kwargs: Must include 'col_name' for the column.
        Returns:
            tuple: (scope, {'rule_col_name': col_name, 'rule_def': rule_def})
        Raises:
            ValueError: If 'col_name' is missing.
        """
        col_name = kwargs.get('col_name', None)

        if col_name is None:
            raise ValueError("Invalid or missing column name")

        rule_def = f"(SUM(CASE WHEN {col_name} = '' THEN 1 ELSE 0 END) / COUNT(*) * 100)"

        return_val = {
            "rule_col_name": col_name,
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val


class ObserveColumnMinTimestamp(ObserveXColumnRuleBase):
    """
    A rule to observe the minimum timestamp value in a specified column.

    Inherits from ObserveXColumnRuleBase. Defines a rule for calculating the earliest timestamp in a given column.
    """
    def __init__(self):
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Defines the rule for the minimum timestamp value in a column.
        Args:
            **kwargs: Must include 'col_name' for the column.
        Returns:
            tuple: (scope, {'rule_def': rule_def})
        Raises:
            ValueError: If 'col_name' is missing.
        """
        col_name = kwargs.get('col_name', None)

        if col_name is None:
            raise ValueError("Invalid or missing column name")

        rule_def = f"MIN({col_name})"

        return_val = {
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val


class ObserveColumnMaxTimestamp(ObserveXColumnRuleBase):
    """
    A rule to observe the maximum timestamp value in a specified column.

    Inherits from ObserveXColumnRuleBase. Defines a rule for calculating the latest timestamp in a given column.
    """
    def __init__(self):
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Defines the rule for the maximum timestamp value in a column.
        Args:
            **kwargs: Must include 'col_name' for the column.
        Returns:
            tuple: (scope, {'rule_def': rule_def})
        Raises:
            ValueError: If 'col_name' is missing.
        """
        col_name = kwargs.get('col_name', None)

        if col_name is None:
            raise ValueError("Invalid or missing column name")

        rule_def = f"MAX({col_name})"

        return_val = {
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val


class ObserveColumnTimestampNullCount(ObserveXColumnRuleBase):
    """
    A rule to observe the count of null timestamp values in a specified column.

    Inherits from ObserveXColumnRuleBase. Defines a rule for calculating the total number of null values in a given timestamp column.
    """
    def __init__(self):
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Defines the rule for counting null timestamp values in a column.
        Args:
            **kwargs: Must include 'col_name' for the column.
        Returns:
            tuple: (scope, {'rule_def': rule_def})
        Raises:
            ValueError: If 'col_name' is missing.
        """
        col_name = kwargs.get('col_name', None)

        if col_name is None:
            raise ValueError("Invalid or missing column name")

        rule_def = f"SUM(CASE WHEN {col_name} IS NULL THEN 1 ELSE 0 END)"

        return_val = {
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val


class ObserveColumnPercentTimestampNullCount(ObserveXColumnRuleBase):
    """
    A rule to observe the percentage of null timestamp values in a specified column.

    Inherits from ObserveXColumnRuleBase. Defines a rule for calculating the percentage of null values in a given timestamp column.
    """
    def __init__(self):
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Defines the rule for calculating the percentage of null timestamp values in a column.
        Args:
            **kwargs: Must include 'col_name' for the column.
        Returns:
            tuple: (scope, {'rule_def': rule_def})
        Raises:
            ValueError: If 'col_name' is missing.
        """
        col_name = kwargs.get('col_name', None)

        if col_name is None:
            raise ValueError("Invalid or missing column name")

        rule_def = f"(SUM(CASE WHEN {col_name} IS NULL THEN 1 ELSE 0 END) / COUNT(*)) * 100"

        return_val = {
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val



"""
    Adding issue related to numeric column
    https://github.com/rapidsai/cudf/issues/4753
"""

class ObserveColumnMinNumeric(ObserveXColumnRuleBase):
    """
    Observation rule class to calculate the minimum value of a numeric column.

    Extends `ObserveXColumnRuleBase` to provide a specific rule for calculating 
    the minimum of a column, excluding NaN values.
    """
    def __init__(self):
        """
        Initializes the ObserveColumnMinNumeric class.

        Calls the constructor of the base class `ObserveXColumnRuleBase` to set up 
        the necessary attributes and context for defining the minimum observation rule.
        """
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Constructs and returns the rule definition for calculating the minimum value of the given column.

        The rule handles NaN values by excluding them from the calculation.

        Parameters:
        - kwargs (dict): Dictionary containing the column name as 'col_name'.

        Returns:
        - tuple: A tuple containing the rule applicability and the rule definition.

        Raises:
        - ValueError: If the 'col_name' is not provided or is invalid.
        """
        col_name = kwargs.get('col_name', None)
        if col_name is None:
            raise ValueError("Invalid or missing column name")

        rule_def = f"MIN(CASE WHEN NOT isnan({col_name}) THEN {col_name} ELSE NULL END)"
        
        return_val = {
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val


class ObserveColumnMaxNumeric(ObserveXColumnRuleBase):
    """
    Observation rule class to calculate the maximum value of a numeric column.

    Extends `ObserveXColumnRuleBase` to provide a specific rule for calculating 
    the maximum value of a column, excluding NaN values.
    """
    def __init__(self):
        """
        Initializes the ObserveColumnMaxNumeric class.

        Calls the constructor of the base class `ObserveXColumnRuleBase` to set up 
        the necessary attributes and context for defining the maximum observation rule.
        """
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Constructs and returns the rule definition for calculating the maximum value of the given column.

        The rule handles NaN values by excluding them from the calculation.

        Parameters:
        - kwargs (dict): Dictionary containing the column name as 'col_name'.

        Returns:
        - tuple: A tuple containing the rule applicability and the rule definition.

        Raises:
        - ValueError: If the 'col_name' is not provided or is invalid.
        """
        col_name = kwargs.get('col_name', None)
        if col_name is None:
            raise ValueError("Invalid or missing column name")

        rule_def = f"MAX(CASE WHEN NOT isnan({col_name}) THEN {col_name} ELSE NULL END)"
        
        return_val = {
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val


class ObserveColumnAvgNumeric(ObserveXColumnRuleBase):
    """
    Observation rule class to calculate the average value of a numeric column.

    Extends `ObserveXColumnRuleBase` to provide a specific rule for calculating 
    the average value of a column, excluding NaN values.
    """
    def __init__(self):
        """
        Initializes the ObserveColumnAvgNumeric class.

        Calls the constructor of the base class `ObserveXColumnRuleBase` to set up 
        the necessary attributes and context for defining the average observation rule.
        """
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Constructs and returns the rule definition for calculating the average value of the given column.

        The rule handles NaN values by excluding them from the calculation.

        Parameters:
        - kwargs (dict): Dictionary containing the column name as 'col_name'.

        Returns:
        - tuple: A tuple containing the rule applicability and the rule definition.

        Raises:
        - ValueError: If the 'col_name' is not provided or is invalid.
        """
        col_name = kwargs.get('col_name', None)
        if col_name is None:
            raise ValueError("Invalid or missing column name")

        rule_def = f"AVG(CASE WHEN NOT isnan({col_name}) THEN {col_name} ELSE NULL END)"
        
        return_val = {
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val


class ObserveColumnStdDevNumeric(ObserveXColumnRuleBase):
    """
    Observation rule class to calculate the standard deviation of a numeric column.

    Extends `ObserveXColumnRuleBase` to provide a specific rule for calculating 
    the standard deviation of a column, excluding NaN values.
    """
    def __init__(self):
        """
        Initializes the ObserveColumnStdDevNumeric class.

        Calls the constructor of the base class `ObserveXColumnRuleBase` to set up 
        the necessary attributes and context for defining the standard deviation observation rule.
        """
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Constructs and returns the rule definition for calculating the standard deviation of the given column.

        The rule handles NaN values by excluding them from the calculation.

        Parameters:
        - kwargs (dict): Dictionary containing the column name as 'col_name'.

        Returns:
        - tuple: A tuple containing the rule applicability and the rule definition.

        Raises:
        - ValueError: If the 'col_name' is not provided or is invalid.
        """
        col_name = kwargs.get('col_name', None)
        if col_name is None:
            raise ValueError("Invalid or missing column name")

        # Define rule for calculating standard deviation
        rule_def = f"STDDEV(CASE WHEN NOT isnan({col_name}) THEN {col_name} ELSE NULL END)"
        
        return_val = {
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val


class ObserveColumnNullCountNumeric(ObserveXColumnRuleBase):
    """
    Observation rule class to calculate the count of NULL values in a numeric column.

    Extends `ObserveXColumnRuleBase` to provide a specific rule for calculating the 
    count of NULL values in a column.
    """
    def __init__(self):
        """
        Initializes the ObserveColumnNullCountNumeric class.

        Calls the constructor of the base class `ObserveXColumnRuleBase` to set up 
        the necessary attributes and context for defining the NULL count observation rule.
        """
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Constructs and returns the rule definition for calculating the count of NULL values in the given column.

        Parameters:
        - kwargs (dict): Dictionary containing the column name as 'col_name'.

        Returns:
        - tuple: A tuple containing the rule applicability and the rule definition.

        Raises:
        - ValueError: If the 'col_name' is not provided or is invalid.
        """
        col_name = kwargs.get('col_name', None)
        if col_name is None:
            raise ValueError("Invalid or missing column name")

        # Define rule for calculating NULL count
        rule_def = f"SUM(CASE WHEN {col_name} IS NULL THEN 1 ELSE 0 END)"
        
        return_val = {
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val


class ObserveColumnZeroCountNumeric(ObserveXColumnRuleBase):
    """
    Observation rule class to calculate the count of zero values in a numeric column.

    Extends `ObserveXColumnRuleBase` to provide a specific rule for calculating the 
    count of zero values in a column.
    """
    def __init__(self):
        """
        Initializes the ObserveColumnZeroCountNumeric class.

        Calls the constructor of the base class `ObserveXColumnRuleBase` to set up 
        the necessary attributes and context for defining the zero count observation rule.
        """
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Constructs and returns the rule definition for calculating the count of zero values in the given column.

        Parameters:
        - kwargs (dict): Dictionary containing the column name as 'col_name'.

        Returns:
        - tuple: A tuple containing the rule applicability and the rule definition.

        Raises:
        - ValueError: If the 'col_name' is not provided or is invalid.
        """
        col_name = kwargs.get('col_name', None)
        if col_name is None:
            raise ValueError("Invalid or missing column name")

        # Define rule for calculating zero count
        rule_def = f"SUM(CASE WHEN {col_name} = 0 THEN 1 ELSE 0 END)"
        
        return_val = {
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val


class ObserveColumnNaNCountNumeric(ObserveXColumnRuleBase):
    """
    Observation rule class to calculate the count of NaN values in a numeric column.

    Extends `ObserveXColumnRuleBase` to provide a specific rule for counting NaN values in the column.
    """
    def __init__(self):
        """
        Initializes the ObserveColumnNaNCountNumeric class.

        Calls the constructor of the base class `ObserveXColumnRuleBase` to set up 
        the necessary attributes and context for defining the NaN count observation rule.
        """
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Constructs and returns the rule definition for calculating the count of NaN values in the given column.

        Parameters:
        - kwargs (dict): Dictionary containing the column name as 'col_name'.

        Returns:
        - tuple: A tuple containing the rule applicability and the rule definition.

        Raises:
        - ValueError: If the 'col_name' is not provided or is invalid.
        """
        col_name = kwargs.get('col_name', None)
        if col_name is None:
            raise ValueError("Invalid or missing column name")

        # Define rule for calculating NaN count
        rule_def = f"SUM(CASE WHEN isnan({col_name}) THEN 1 ELSE 0 END)"
        
        return_val = {
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val


class ObserveColumnApproxDistinctCountNumeric(ObserveXColumnRuleBase):
    """
    Observation rule class to calculate the approximate distinct count of values in a numeric column.

    Extends `ObserveXColumnRuleBase` to provide a specific rule for calculating an approximate count
    of distinct values in the column.
    """
    def __init__(self):
        """
        Initializes the ObserveColumnApproxDistinctCountNumeric class.

        Calls the constructor of the base class `ObserveXColumnRuleBase` to set up 
        the necessary attributes and context for defining the approximate distinct count observation rule.
        """
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Constructs and returns the rule definition for calculating the approximate distinct count 
        of values in the given column.

        Parameters:
        - kwargs (dict): Dictionary containing the column name as 'col_name'.

        Returns:
        - tuple: A tuple containing the rule applicability and the rule definition.

        Raises:
        - ValueError: If the 'col_name' is not provided or is invalid.
        """
        col_name = kwargs.get('col_name', None)
        if col_name is None:
            raise ValueError("Invalid or missing column name")

        # Define rule for calculating approximate distinct count
        rule_def = f"approx_count_distinct({col_name})"
        
        return_val = {
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val


class ObserveColumnMedianNumeric(ObserveXColumnRuleBase):
    """
    Observation rule class for calculating the median value of a numeric column.

    Extends `ObserveXColumnRuleBase` to provide a specific rule for calculating the median using 
    the `percentile_approx` function.
    """
    def __init__(self):
        """
        Initializes the ObserveColumnMedianNumeric class.

        Calls the constructor of the base class `ObserveXColumnRuleBase` to set up
        the necessary attributes and context for defining the median observation rule.
        """
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Constructs and returns the rule definition for calculating the median value
        of the given numeric column using the `percentile_approx` function.

        Parameters:
        - kwargs (dict): Dictionary containing the column name as 'col_name'.

        Returns:
        - tuple: A tuple containing the rule applicability and the rule definition.

        Raises:
        - ValueError: If the 'col_name' is not provided or is invalid.
        """
        col_name = kwargs.get('col_name', None)
        if col_name is None:
            raise ValueError("Invalid or missing column name")

        # Define rule for calculating the median using percentile_approx function
        rule_def = f"percentile_approx({col_name}, 0.5)"
        
        return_val = {
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val


class ObserveColumnPercentNullNumeric(ObserveXColumnRuleBase):
    """
    Observation rule class for calculating the percentage of NULL values in a numeric column.

    Extends `ObserveXColumnRuleBase` to provide a specific rule for determining the proportion of
    NULL values in the specified column.
    """
    def __init__(self):
        """
        Initializes the ObserveColumnPercentNullNumeric class.

        Calls the constructor of the base class `ObserveXColumnRuleBase` to set up
        the necessary attributes and context for defining the NULL percentage observation rule.
        """
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Constructs and returns the rule definition for calculating the percentage of NULL values
        in the given numeric column.

        Parameters:
        - kwargs (dict): Dictionary containing the column name as 'col_name'.

        Returns:
        - tuple: A tuple containing the rule applicability and the rule definition.

        Raises:
        - ValueError: If the 'col_name' is not provided or is invalid.
        """
        col_name = kwargs.get('col_name', None)
        if col_name is None:
            raise ValueError("Invalid or missing column name")

        # Define rule for calculating the percentage of NULL values
        rule_def = f"(SUM(CASE WHEN {col_name} IS NULL THEN 1 ELSE 0 END) / COUNT(*)) * 100"
        
        return_val = {
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val


class ObserveColumnPercentZeroNumeric(ObserveXColumnRuleBase):
    """
    Observation rule class for calculating the percentage of zero values in a numeric column.

    Extends `ObserveXColumnRuleBase` to provide a specific rule for determining the proportion of
    zero values in the specified column.
    """
    def __init__(self):
        """
        Initializes the ObserveColumnPercentZeroNumeric class.

        Calls the constructor of the base class `ObserveXColumnRuleBase` to set up
        the necessary attributes and context for defining the zero percentage observation rule.
        """
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Constructs and returns the rule definition for calculating the percentage of zero values
        in the given numeric column.

        Parameters:
        - kwargs (dict): Dictionary containing the column name as 'col_name'.

        Returns:
        - tuple: A tuple containing the rule applicability and the rule definition.

        Raises:
        - ValueError: If the 'col_name' is not provided or is invalid.
        """
        col_name = kwargs.get('col_name', None)
        if col_name is None:
            raise ValueError("Invalid or missing column name")

        # Define rule for calculating the percentage of zero values
        rule_def = f"(SUM(CASE WHEN {col_name} = 0 THEN 1 ELSE 0 END) / COUNT(*)) * 100"
        
        return_val = {
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val


class ObserveColumnPercentNaNNumeric(ObserveXColumnRuleBase):
    """
    Observation rule class for calculating the percentage of NaN values in a numeric column.

    Extends `ObserveXColumnRuleBase` to provide a specific rule for determining the proportion of
    NaN values in the specified column.
    """
    def __init__(self):
        """
        Initializes the ObserveColumnPercentNaNNumeric class.

        Calls the constructor of the base class `ObserveXColumnRuleBase` to set up
        the necessary attributes and context for defining the NaN percentage observation rule.
        """
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Constructs and returns the rule definition for calculating the percentage of NaN values
        in the given numeric column.

        Parameters:
        - kwargs (dict): Dictionary containing the column name as 'col_name'.

        Returns:
        - tuple: A tuple containing the rule applicability and the rule definition.

        Raises:
        - ValueError: If the 'col_name' is not provided or is invalid.
        """
        col_name = kwargs.get('col_name', None)
        if col_name is None:
            raise ValueError("Invalid or missing column name")

        # Define rule for calculating the percentage of NaN values
        rule_def = f"(SUM(CASE WHEN isnan({col_name}) THEN 1 ELSE 0 END) / COUNT(*)) * 100"

        return_val = {
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val



class ObserveColumnArrayNullCount(ObserveXColumnRuleBase):
    """
    A rule to observe the count of null values within arrays in a specified column.

    Inherits from ObserveXColumnRuleBase. Defines a rule for calculating the count of null 
    values inside array elements in the given column.
    """
    def __init__(self):
        """
        Initializes the ObserveColumnArrayNullCount class.

        Calls the constructor of the base class `ObserveXColumnRuleBase` to set up
        the necessary attributes and context for defining the null count observation rule in arrays.
        """
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Defines the rule for calculating the count of null values within an array column.

        Args:
            **kwargs: Must include 'col_name' for the column.

        Returns:
            tuple: (scope, {'rule_def': rule_def})

        Raises:
            ValueError: If 'col_name' is missing.
        """
        col_name = kwargs.get('col_name', None)

        if col_name is None:
            raise ValueError("Invalid or missing column name")

        rule_def = f"SUM(CASE WHEN size({col_name}) = 0 THEN 1 ELSE aggregate({col_name}, 0, (temp, x) -> temp + IF(x IS NULL, 1, 0)) END)"
 
        return_val = {
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val

class ObserveColumnArrayNullPercent(ObserveXColumnRuleBase):
    """
    A rule to observe the percentage of null values within arrays in a specified column.

    Inherits from ObserveXColumnRuleBase. Defines a rule for calculating the percentage of null 
    values inside array elements in the given column.
    """
    def __init__(self):
        """
        Initializes the ObserveColumnArrayNullPercent class.

        Calls the constructor of the base class `ObserveXColumnRuleBase` to set up
        the necessary attributes and context for defining the null percentage observation rule in arrays.
        """
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Defines the rule for calculating the percentage of null values within an array column.

        Args:
            **kwargs: Must include 'col_name' for the column.

        Returns:
            tuple: (scope, {'rule_def': rule_def})

        Raises:
            ValueError: If 'col_name' is missing.
        """
        col_name = kwargs.get('col_name', None)

        if col_name is None:
            raise ValueError("Invalid or missing column name")

        rule_def = f"(SUM(CASE WHEN size({col_name}) = 0 THEN 1 ELSE aggregate({col_name}, 0, (temp, x) -> temp + IF(x IS NULL, 1, 0)) END) / COUNT(*)) * 100"
 
        return_val = {
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val


class ObserveColumnSetNullCount(ObserveXColumnRuleBase):
    """
    A rule to observe the count of null values within sets in a specified column.

    Inherits from ObserveXColumnRuleBase. Defines a rule for calculating the count of null 
    values inside set elements in the given column.
    """
    def __init__(self):
        """
        Initializes the ObserveColumnSetNullCount class.

        Calls the constructor of the base class `ObserveXColumnRuleBase` to set up
        the necessary attributes and context for defining the null count observation rule in sets.
        """
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Defines the rule for calculating the count of null values within a set column.

        Args:
            **kwargs: Must include 'col_name' for the column.

        Returns:
            tuple: (scope, {'rule_def': rule_def})

        Raises:
            ValueError: If 'col_name' is missing.
        """
        col_name = kwargs.get('col_name', None)

        if col_name is None:
            raise ValueError("Invalid or missing column name")

        # Rule definition to count the number of null values in a set column
        rule_def = f"SUM(CASE WHEN size({col_name}) = 0 THEN 1 ELSE aggregate(transform({col_name}, x -> CASE WHEN x IS NULL THEN 1 ELSE 0 END), 0, (temp, x) -> temp + x)END)"
 
        return_val = {
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val

class ObserveColumnSetNullPercent(ObserveXColumnRuleBase):
    """
    A rule to observe the percentage of null values within sets in a specified column.

    Inherits from ObserveXColumnRuleBase. Defines a rule for calculating the percentage of null 
    values inside set elements in the given column.
    """
    def __init__(self):
        """
        Initializes the ObserveColumnSetNullPercent class.

        Calls the constructor of the base class `ObserveXColumnRuleBase` to set up
        the necessary attributes and context for defining the null percentage observation rule in sets.
        """
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Defines the rule for calculating the percentage of null values within a set column.

        Args:
            **kwargs: Must include 'col_name' for the column.

        Returns:
            tuple: (scope, {'rule_def': rule_def})

        Raises:
            ValueError: If 'col_name' is missing.
        """
        col_name = kwargs.get('col_name', None)

        if col_name is None:
            raise ValueError("Invalid or missing column name")

        # Rule definition to calculate the percentage of null values in a set column
        rule_def = f"(SUM(CASE WHEN size({col_name}) = 0 THEN 1 ELSE aggregate(transform({col_name}, x -> CASE WHEN x IS NULL THEN 1 ELSE 0 END), 0, (temp, x) -> temp + x)END) / COUNT(*)) * 100"
 
        return_val = {
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val



class ObserveColumnArrayMaxLen(ObserveXColumnRuleBase):
    """
    A rule to observe the percentage of null timestamp values in a specified column.

    Inherits from ObserveXColumnRuleBase. Defines a rule for calculating the percentage of null values in a given timestamp column.
    """
    def __init__(self):
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Defines the rule for calculating the percentage of null timestamp values in a column.
        Args:
            **kwargs: Must include 'col_name' for the column.
        Returns:
            tuple: (scope, {'rule_def': rule_def})
        Raises:
            ValueError: If 'col_name' is missing.
        """
        col_name = kwargs.get('col_name', None)

        if col_name is None:
            raise ValueError("Invalid or missing column name")

        rule_def = f"MAX(ARRAY_MAX(transform({col_name}, x -> length(x))))"

        return_val = {
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val

class ObserveColumnArrayMinLen(ObserveXColumnRuleBase):
    """
    A rule to observe the percentage of null timestamp values in a specified column.

    Inherits from ObserveXColumnRuleBase. Defines a rule for calculating the percentage of null values in a given timestamp column.
    """
    def __init__(self):
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Defines the rule for calculating the percentage of null timestamp values in a column.
        Args:
            **kwargs: Must include 'col_name' for the column.
        Returns:
            tuple: (scope, {'rule_def': rule_def})
        Raises:
            ValueError: If 'col_name' is missing.
        """
        col_name = kwargs.get('col_name', None)

        if col_name is None:
            raise ValueError("Invalid or missing column name")

        rule_def = f"MIN(ARRAY_MIN(transform({col_name}, x -> length(x))))"

        return_val = {
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val

class ObserveColumnArrayAvgLen(ObserveXColumnRuleBase):
    """
    A rule to observe the percentage of null timestamp values in a specified column.

    Inherits from ObserveXColumnRuleBase. Defines a rule for calculating the percentage of null values in a given timestamp column.
    """
    def __init__(self):
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Defines the rule for calculating the percentage of null timestamp values in a column.
        Args:
            **kwargs: Must include 'col_name' for the column.
        Returns:
            tuple: (scope, {'rule_def': rule_def})
        Raises:
            ValueError: If 'col_name' is missing.
        """
        col_name = kwargs.get('col_name', None)

        if col_name is None:
            raise ValueError("Invalid or missing column name")

        rule_def = f"AVG(aggregate(transform({col_name}, x -> length(x)), 0, (temp, x) -> temp + x) / size({col_name}))"

        return_val = {
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val











