"""
This module contains classes and methods for managing row-level observation rules within the ObserveX framework.
"""
from pyspark.sql.functions import *
from observex.core import base as oxb, utils as u
from observex.observers import observerbase as ob
import re

class ObserveXRowRuleFactory(oxb.ObserveXGlobalBase):
    """
    Factory class for dynamically creating instances of row observation rule classes.

    This class handles the instantiation of row observation rule classes based on their names. It normalizes 
    class names to handle various naming conventions and ensures that the correct class is returned if it is 
    found in the global context.

    Methods:
    - `get_instance(name)`: Finds and returns an instance of the row rule class specified by `name`. Raises 
      `NotImplementedError` or `NameError` if the class is not found or not implemented.

    - `_normalize_class_name(name)`: Normalizes the class name by handling different variations and naming 
      conventions.
    """
    
    def __init__(self):
        """
        Initializes the `ObserveXRowRuleFactory` class.
        """
        super().__init__()

    def get_instance(self, name):
        """
        Finds and returns an instance of the row rule class specified by `name`.

        This method normalizes the class name and attempts to find and instantiate a class in the global context 
        with a matching name. It raises an error if the class is not found or does not inherit from 
        `ObserveXRowRuleBase`.

        Parameters:
        - name (str): The name of the row rule class to be instantiated.

        Returns:
        - An instance of the row rule class.

        Raises:
        - NotImplementedError: If the class is not implemented or does not inherit from `ObserveXRowRuleBase`.
        - NameError: If the class is not found in the global context.
        """
        normalized_name = self._normalize_class_name(name)
        for class_name in globals():
            if class_name.lower() == normalized_name.lower():
                obj = globals()[class_name]
                if issubclass(obj, ObserveXRowRuleBase):
                    return obj()
                else:
                    oxb.logging.debug(f"[{name}] is not found OR is not implemented.")
                    raise NotImplementedError(f"[{name}] is not found OR is not implemented.")

        oxb.logging.error(f"[{normalized_name}] is not found OR is not implemented in global context.")
        raise NameError(f"[{normalized_name}] is not found OR is not implemented in global context.")

    def _normalize_class_name(self, name):
        """
        Normalizes the rule class name by handling various naming conventions.

        This method handles different variations of class names, including those with underscores, hyphens, 
        and different cases. It ensures that the class name follows a consistent format.

        Parameters:
        - name (str): The class name to be normalized.

        Returns:
        - str: The normalized class name with 'Observe' prefix.
        """
        name = name.replace('Observe', '').strip()
        name_parts = re.split(r'[_\s-]', name)
        normalized_name = ''.join([part[:1].upper() + part[1:] if part else '' for part in name_parts])
        return f"Observe{normalized_name}"


class ObserveXRowRuleBase(ob.ObserveXRuleBase):
    """
    Base class for defining row-level observation rules in ObserveX.

    This class provides the core interface for row-level rules. It defines methods that must be implemented 
    in subclasses to create specific row-level observation logic. The class also includes methods for generating 
    rule-specific column names.

    Attributes:
    - _rule_applies_to (str): Indicates that the rule applies to "row".

    Methods:
    - __init__(): Initializes the base class and sets the rule applicability to "row".

    - observation_rule(**kwargs): Abstract method to be implemented in subclasses to define row-level 
      observation logic. Raises a `NotImplementedError` if not overridden.

    - _get_rule_col_name(col_name): Generates a standardized column name based on the rule class and 
      the provided column name.
    """
    
    def __init__(self):
        """
        Initializes the `ObserveXRowRuleBase` class by setting the `_rule_applies_to` attribute to "row".
        """
        super().__init__()
        self._rule_applies_to = "row"

    def observation_rule(self, **kwargs):
        """
        Abstract method to be implemented in subclasses for row-level observation logic.

        This method is called when the rule is triggered and should return a dictionary containing the 
        observation data. It raises a `NotImplementedError` if not overridden in a subclass.

        Parameters:
        - **kwargs: Arbitrary keyword arguments to be used by the subclass implementation.

        Raises:
        - NotImplementedError: If not implemented in the subclass.
        """
        oxb.logging.error("observation_rule must be implemented by the subclass.")
        raise NotImplementedError("Not implemented in base-class. Must be implemented in sub-class")
    
    def _get_rule_col_name(self, col_name):
        """
        Generates a standardized column name for the rule.

        This method creates a column name that incorporates the rule class name and the original column name. 
        It is used to uniquely identify columns related to the rule in the dataset.

        Parameters:
        - col_name (str): The original column name.

        Returns:
        - str: A standardized column name in the format `__ox_<col_name>_<rule_class_name>__`.
        """
        return f"__ox_{col_name}_{type(self).__name__}__"


class ObserveColumnLengthBetween(ObserveXRowRuleBase):
    """
        Initializes the ObserveColumnLengthBetween class.
        This constructor calls the superclass constructor to inherit all functionalities from 
        `ObserveXRowRuleBase`.
        
    """
    def __init__(self):
        super().__init__()


    """
    Generates the SQL expression for validating the length of the values in a column.
        
        Args:
            col_name (str): The name of the column to apply the rule.
            min_len (int): The minimum length allowed for the column's values.
            max_len (int): The maximum length allowed for the column's values.
        
        Returns:
            str: The rule applies to the "row" and a dictionary containing:
                 - rule_col_name: The generated column name for validation.
                 - rule_def: The SQL expression used for the validation.
    """

    def observation_rule(self, **kwargs):
        col_name = kwargs.get('col_name', None)
        min_len = kwargs.get('min_len', None)
        max_len = kwargs.get('max_len', None)
        
        if col_name is None:
            raise ValueError(f"Invalid values passed for parameters col_name: None")
        if min_len is None:
            raise ValueError(f"Invalid values passed for parameters min_len: None")
        if max_len is None:
            raise ValueError(f"Invalid values passed for parameters max_len: None")
        rule_def = f"CASE WHEN LENGTH({col_name}) BETWEEN {min_len} AND {max_len} THEN NULL ELSE 'Length of {col_name} is not between {min_len} and {max_len}' END"
        
        return_val = {
            "rule_col_name": self._get_rule_col_name(col_name),
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val

class ObserveMultiFieldSumToEqual(ObserveXRowRuleBase):
    def __init__(self):
        super().__init__()

    """
    :param columns: list of column names to sum
    :param target_column: target column name to compare the sum

    :returns: returns a dictionary of values: ("rule_col_name", "rule_def", "rule_applies_to")
    """
    def observation_rule(self, **kwargs):
        columns = kwargs.get('columns', None)
        target_column = kwargs.get('target_column', None)
        
        if not columns or not isinstance(columns, list):
            raise ValueError("Invalid or missing parameter 'columns'. It should be a list of column names.")
        
        if target_column is None:
            raise ValueError("Invalid values passed for parameter target_column: None")
        sum_expr = " + ".join(columns)
        
        return_val = {}
        return_val["rule_col_name"] = self._get_rule_col_name(f"{'_'.join(columns)}_sum_vs_{target_column}")
        return_val["rule_def"] = f"CASE WHEN ({sum_expr}) = {target_column} THEN NULL ELSE '{sum_expr} is not equal to {target_column}' END"

        return self._rule_applies_to, return_val



class ObserveFieldValueBetween(ObserveXRowRuleBase):
    def __init__(self):
        super().__init__()

    """
    :param col_name: column name where the rule is applied
    :param min_val: minimum value
    :param max_val: maximum value

    :returns: returns a dictionary of values: ("rule_col_name", "rule_def", "rule_applies_to")
    """
    def observation_rule(self, **kwargs):
        col_name = kwargs.get('col_name', None)
        min_val = kwargs.get('min_val', None)
        max_val = kwargs.get('max_val', None)
        
        if col_name is None:
            raise ValueError("Invalid or missing parameter 'col_name'.")
        
        if min_val is None or max_val is None:
            raise ValueError("Both 'min_val' and 'max_val' must be provided.")
        
       
        condition_expr = f"{col_name} BETWEEN {min_val} AND {max_val}"
        
        rule_col_name = self._get_rule_col_name(f"{col_name}_between_{min_val}_and_{max_val}")
        rule_def = f"CASE WHEN {condition_expr} THEN NULL ELSE 'Value of {col_name} is not between {min_val} and {max_val}' END"
        
        return self._rule_applies_to, {
            "rule_col_name": rule_col_name,
            "rule_def": rule_def
        }



class ObserveSetExpectation(ObserveXRowRuleBase):
    def __init__(self):
        super().__init__()

    """
    :param col_name: column name where this rule is applied
    :param valid_set: list of valid values

    :returns: returns a dictionary of values: ("rule_col_name", "rule_def", "rule_applies_to")
    """
    def observation_rule(self, **kwargs):
        col_name = kwargs.get('col_name', None)
        valid_set = kwargs.get('valid_set', None)
        
        if col_name is None:
            raise ValueError("Invalid or missing parameter 'col_name'.")
        
        if valid_set is None or not isinstance(valid_set, list):
            raise ValueError("Invalid or missing parameter 'valid_set'. It should be a list of valid values.")
        
        
        valid_set_str = ', '.join([f"'{val}'" for val in valid_set])
        rule_def = f"CASE WHEN {col_name} IN ({valid_set_str}) THEN NULL ELSE 'Value in {col_name} is not in the valid set' END"
        
        return self._rule_applies_to, {
            "rule_col_name": self._get_rule_col_name(col_name),
            "rule_def": rule_def
        }


class ObserveColumnValueForEmail(ObserveXRowRuleBase):
    def __init__(self):
        super().__init__()

    """
    :param col_name: column name where this rule is applied

    :returns: returns a dictionary of values: ("rule_col_name", "rule_def", "rule_applies_to")
    """
    def observation_rule(self, **kwargs):
        col_name = kwargs.get('col_name', None)

        if col_name is None:
            raise ValueError("Invalid or missing parameter 'col_name'.")

        
        email_pattern = "[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,6}"

        
        rule_def = f"CASE WHEN {col_name} RLIKE '{email_pattern}' THEN NULL ELSE 'Invalid email format in {col_name}' END"

        return_val = {
            "rule_col_name": self._get_rule_col_name(col_name),
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val



class ObserveColumnValueForUuid(ObserveXRowRuleBase):
    def __init__(self):
        super().__init__()

    """
    :param col_name: column name where this rule is applied

    :returns: returns a dictionary of values: ("rule_col_name", "rule_def", "rule_applies_to")
    """
    def observation_rule(self, **kwargs):
        col_name = kwargs.get('col_name', None)

        if col_name is None:
            raise ValueError("Invalid or missing parameter 'col_name'.")

        
        uuid_pattern = "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"

        
        rule_def = f"CASE WHEN {col_name} RLIKE '{uuid_pattern}' THEN NULL ELSE 'Invalid UUID format in {col_name}' END"

        return_val = {
            "rule_col_name": self._get_rule_col_name(col_name),
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val



class ObserveColumnValueForPattern(ObserveXRowRuleBase):
    """
    This rule class validates if the column values match a given pattern using regular expressions.
    """

    def __init__(self):
        """
        Initializes the ObserveColumnValueForPattern class.
        """
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Generates a SQL rule to validate if a column value matches the given regular expression pattern.

        :param col_name: The column name to be checked.
        :param regex_pattern: The regular expression pattern to validate against.
        
        :returns: A tuple containing the rule application type and a dictionary with the rule definition and column name.
        """

        col_name = kwargs.get('col_name', None)
        regex_pattern = kwargs.get('regex_pattern', None)

        if col_name is None:
            raise ValueError("Invalid or missing parameter 'col_name'.")
        
        if regex_pattern is None:
            raise ValueError("Invalid or missing parameter 'regex_pattern'.")

        
        rule_def = f"CASE WHEN {col_name} RLIKE '{regex_pattern}' THEN NULL ELSE 'Value in {col_name} does not match the pattern' END"

        return_val = {
            "rule_col_name": self._get_rule_col_name(col_name),
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val



class ObserveColumnForNullValue(ObserveXRowRuleBase):

    def __init__(self):
        """
        Initializes the ObserveNullCheck class by calling the constructor of 
        its superclass, ObserveXRowRuleBase.
        """
        super().__init__()
        print("ObserveNullCheck")

    def observation_rule(self, **kwargs):
        """
        Generates a SQL rule to detect null, empty values, or placeholder values (e.g., "null") in one or more specified columns.
        
        If multiple columns are provided, the rule checks each column for null/empty/placeholder values.
        
        :param col_names: list of column names where the null check is applied
        :param null_placeholders: optional list of placeholder strings (e.g., "null") to treat as null values
        
        :returns: a dictionary with the generated rule definition and rule column name
        """
        col_names = kwargs.get('col_names', None)
        null_placeholders = kwargs.get('null_placeholders', ["null", "NULL"]) 
        if col_names is None or not isinstance(col_names, list):
            raise ValueError("Invalid or missing parameter 'col_names'. It should be a list of column names.")

        
        case_statements = []
        for col_name in col_names:
           
            case_statements.append(
                f"CASE WHEN {col_name} IS NULL OR {col_name} = '' OR {col_name} IN ({', '.join([repr(val) for val in null_placeholders])}) "
                f"THEN 'NULL/Empty in {col_name}' ELSE NULL END"
)


        
        rule_def = "array(" + ", ".join(case_statements) + ")"

        
        return_val = {
            "rule_col_name": self._get_rule_col_name("_".join(col_names) + "_null_check"),
            "rule_def": f"""
                CASE WHEN size(filter({rule_def}, x -> x IS NOT NULL)) > 0 
                     THEN filter({rule_def}, x -> x IS NOT NULL) 
                     ELSE NULL 
                END
            """
        }

        return self._rule_applies_to, return_val




class ObserveColumnForSetValues(ObserveXRowRuleBase):
    def __init__(self):
        """
        Initializes the ObserveColumnForSetValues class, which checks for 
        single quotes, double quotes, or multiple double quotes in a specified column.
        """
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Generates a SQL rule to detect double quotes, single quotes, and multiple double quotes.
        
        :param col_name: The column name to check for quotes
        :returns: A dictionary containing rule column name and SQL expression (rule_def)
        """
        col_name = kwargs.get('col_name', None)
        if col_name is None:
            raise ValueError("Invalid or missing parameter 'col_name'.")

        
        rule_def = f"""
            CASE 
                WHEN {col_name} LIKE '%"%' THEN 'Double quotes in {col_name}'
                WHEN {col_name} LIKE '%\\\'%' THEN 'Single quotes in {col_name}'
                ELSE NULL 
            END
        """

        return_val = {
            "rule_col_name": self._get_rule_col_name(col_name),
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val




class ObserveColumnForDomainValues(ObserveXRowRuleBase):
    def __init__(self):
        super().__init__()

    """
    :param col_name: column name where this rule is applied
    :param domain: domain value to check in the column (example: '@gmail.com')

    :returns: returns a dictionary of values: ("rule_col_name", "rule_def", "rule_applies_to")
    """
    def observation_rule(self, **kwargs):
        col_name = kwargs.get('col_name', None)
        domain = kwargs.get('domain', None)

        if col_name is None:
            raise ValueError("Invalid or missing parameter 'col_name'.")

        if domain is None:
            raise ValueError("Invalid or missing parameter 'domain'.")

       
        rule_def = f"CASE WHEN {col_name} LIKE '%@{domain}' THEN NULL ELSE 'Invalid domain value in {col_name}' END"

        return_val = {
            "rule_col_name": self._get_rule_col_name(col_name),
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val


class ObserveColumnValueForCamelcase(ObserveXRowRuleBase):

    def __init__(self):
        """
        Initializes the ObserveColumnValueForCamelcase class by calling the constructor of
        its superclass, ObserveXRowRuleBase.
        """
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Generates a SQL rule to validate if all values in a specified column are in camel case.

        :param kwargs: keyword arguments containing 'col_name' which is the name of the column to check.
        :returns: a tuple containing a dictionary of values ("rule_col_name", "rule_def") and "rule_applies_to".
        :raises ValueError: if 'col_name' is missing or None.
        """
        col_name = kwargs.get('col_name')

        if col_name is None:
            raise ValueError("Invalid values passed for parameter col_name: None")

        rule_def = (
            f"CASE WHEN {col_name} REGEXP '^[A-Z][a-zA-Z]*([A-Z][a-zA-Z]*)*$' "
            f"THEN NULL ELSE 'Value in {col_name} is not camel case' END"
        )

        return_val = {
            "rule_col_name": self._get_rule_col_name(col_name),
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val
    


class ObserveColumnValueForLowercase(ObserveXRowRuleBase):

    def __init__(self):
        """
        Initializes the ObserveColumnValueForLowercase class by calling the constructor of
        its superclass, ObserveXRowRuleBase.
        """
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Generates a SQL rule to validate if all values in a specified column are lowercase.

        :param kwargs: keyword arguments containing 'col_name' which is the name of the column to check.
        :returns: a tuple containing a dictionary of values ("rule_col_name", "rule_def") and "rule_applies_to".
        :raises ValueError: if 'col_name' is missing or None.
        """
        col_name = kwargs.get('col_name')

        if col_name is None:
            raise ValueError("Invalid values passed for parameter col_name: None")

        rule_def = (
            f"CASE WHEN {col_name} = LOWER({col_name}) "
            f"THEN NULL ELSE 'Value in {col_name} is not lowercase' END"
        )

        return_val = {
            "rule_col_name": self._get_rule_col_name(col_name),
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val
    


class ObserveColumnValueForUppercase(ObserveXRowRuleBase):

    def __init__(self):
        """
        Initializes the ObserveColumnValueForUppercase class by calling the constructor of
        its superclass, ObserveXRowRuleBase.
        """
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Generates a SQL rule to validate if all values in a specified column are uppercase.

        :param kwargs: keyword arguments containing 'col_name' which is the name of the column to check.
        :returns: a tuple containing a dictionary of values ("rule_col_name", "rule_def") and "rule_applies_to".
        :raises ValueError: if 'col_name' is missing or None.
        """
        col_name = kwargs.get('col_name')

        if col_name is None:
            raise ValueError("Invalid values passed for parameter col_name: None")

        rule_def = (
            f"CASE WHEN {col_name} = UPPER({col_name}) "
            f"THEN NULL ELSE 'Value in {col_name} is not uppercase' END"
        )

        return_val = {
            "rule_col_name": self._get_rule_col_name(col_name),
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val
    


"""
A class that checks for duplicate values in a specified column.

This class inherits from the ObserveXRowRuleBase and provides functionality
to generate a rule for detecting duplicate rows based on the values in a specified column.
It raises a ValueError if the column name is missing or invalid.
"""

class ObserveUniquenessCheck(ObserveXRowRuleBase):

    def __init__(self):
        """
        Initializes the ObserveUniquenessCheck class by calling the constructor of 
        its superclass, ObserveXRowRuleBase.
        """
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Generates a SQL rule to detect duplicate values in a specified column.

        """
        col_name = kwargs.get('col_name', None)

        if col_name is None:
            raise ValueError("Invalid or missing parameter 'col_name'.")

        rule_def = f"CASE WHEN COUNT(*) OVER (PARTITION BY {col_name}) > 1 THEN 'Duplicate Rows' ELSE NULL END"

        return_val = {
            "rule_col_name": self._get_rule_col_name(col_name),
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val



"""
A class that checks for special characters in a specified column.

This class inherits from the ObserveXRowRuleBase and provides functionality
to generate a rule for detecting special characters within the values of a specified column.
It raises a ValueError if the column name is missing or invalid.
"""

class ObserveSpecialCharacterCheck(ObserveXRowRuleBase):

    def __init__(self):
        """
        Initializes the ObserveSpecialCharacterCheck class by calling the constructor of 
        its superclass, ObserveXRowRuleBase.
        """
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Generates a SQL rule to detect special characters in a specified column.
        """
        col_name = kwargs.get('col_name', None)
        
        if col_name is None:
            raise ValueError("Invalid or missing parameter 'col_name'.")

       
        special_chars_pattern = r'[!@#$%^&*()+=<>|{}`~/-]'
        
       
        rule_def = f"""
        CASE 
            WHEN {col_name} RLIKE '{special_chars_pattern}' 
            THEN '{col_name} contains special characters'
            ELSE NULL
        END
        """

        return_val = {
            "rule_col_name": self._get_rule_col_name(col_name),
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val



"""
A class that checks if the length of values in a specified column meets the minimum length requirement.

This class inherits from the ObserveXRowRuleBase and provides functionality
to generate a rule for ensuring that the length of values in a specified column 
is greater than or equal to a given minimum length. It raises a ValueError if 
the column name or minimum length is missing or invalid.
"""
class ObserveColumnMinLength(ObserveXRowRuleBase):

    def __init__(self):
        """
        Initializes the ObserveColumnMinLength class by calling the constructor of 
        its superclass, ObserveXRowRuleBase.
        """
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Generates a SQL rule to check if the length of values in a specified column 
        meets the minimum length requirement.
        """
        col_name = kwargs.get('col_name', None)
        min_len = kwargs.get('min_len', None)

        if col_name is None:
            raise ValueError("Invalid or missing column name")
        if min_len is None:
            raise ValueError("Minimum Length must be provided")

        rule_def = f"CASE WHEN LENGTH({col_name}) >= {min_len} THEN NULL ELSE 'The length of the {col_name} is lesser than the minimum length' END"

        return_val = {
            "rule_col_name": self._get_rule_col_name(col_name),
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val



"""
A class that checks if the length of values in a specified column does not exceed
the maximum length requirement.

This class inherits from the ObserveXRowRuleBase and provides functionality
to generate a rule for ensuring that the length of values in a specified column 
is less than or equal to a given maximum length. It raises a ValueError if 
the column name or maximum length is missing or invalid.
"""
class ObserveColumnMaxLength(ObserveXRowRuleBase):

    def __init__(self):
        """
        Initializes the ObserveColumnMaxLength class by calling the constructor of 
        its superclass, ObserveXRowRuleBase.
        """
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Generates a SQL rule to check if the length of values in a specified column 
        does not exceed the maximum length requirement.

        """
        col_name = kwargs.get('col_name', None)
        max_len = kwargs.get('max_len', None)

        if col_name is None:
            raise ValueError("Invalid or missing column name")
        if max_len is None:
            raise ValueError("Maximum Length must be provided")

        rule_def = f"CASE WHEN LENGTH({col_name}) <= {max_len} THEN NULL ELSE 'The length of the {col_name} is greater than the maximum length' END"

        return_val = {
            "rule_col_name": self._get_rule_col_name(col_name),
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val



class ObserveColumnValueForKebabcase(ObserveXRowRuleBase):
    def __init__(self):
        super().__init__()

    """
    Kebab case is a naming convention that uses hyphens to replace spaces between words, 
    and typically uses lowercase letters throughout
    
    :param col_name: column name where this rule is applied
    :returns: returns a dictionary of values: ("rule_col_name", "rule_def", "rule_applies_to")
    """
    def observation_rule(self, **kwargs):
        col_name = kwargs.get('col_name', None)

        if col_name is None:
            raise ValueError("Invalid or missing parameter 'col_name'.")

       
        kebabcase_pattern = "^[a-z0-9]+(-[a-z0-9]+)*$"

        
        rule_def = f"CASE WHEN {col_name} RLIKE '{kebabcase_pattern}' THEN NULL ELSE 'Invalid kebab-case format in {col_name}' END"

        return_val = {
            "rule_col_name": self._get_rule_col_name(col_name),
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val




"""
A class that checks if the values in a specified column adhere to the snake_case format.

This class inherits from ObserveXRowRuleBase and provides functionality
to generate a rule for ensuring that the values in a specified column follow
the snake_case naming convention. It raises a ValueError if the column name is
missing or invalid.
"""
class ObserveColumnValueForSnakecase(ObserveXRowRuleBase):

    def __init__(self):
        """
        Initializes the ObserveColumnValueForSnakecase class by calling the constructor of 
        its superclass, ObserveXRowRuleBase.
        """
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Generates a SQL rule to check if the values in a specified column follow
        the snake_case naming convention.
        """
        col_name = kwargs.get('col_name', None)

        if col_name is None:
            raise ValueError("Invalid or Missing Column Name")

        snake_case = r"'^[a-z]+([_a-z]+)*$'"
        rule_def = f"CASE WHEN {col_name} RLIKE {snake_case} THEN NULL ELSE '{col_name} is not in Snake Case' END"

        return_val = {
            "rule_col_name": self._get_rule_col_name(col_name),
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val



"""
A class that checks if the values in a specified column adhere to the PascalCase format.

This class inherits from ObserveXRowRuleBase and provides functionality
to generate a rule for ensuring that the values in a specified column follow
the PascalCase naming convention. It raises a ValueError if the column name is
missing or invalid.
"""
class ObserveColumnValueForPascalcase(ObserveXRowRuleBase):

    def __init__(self):
        """
        Initializes the ObserveColumnValueForPascalcase class by calling the constructor of 
        its superclass, ObserveXRowRuleBase.
        """
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Generates a SQL rule to check if the values in a specified column follow
        the PascalCase naming convention.
        """
        col_name = kwargs.get('col_name', None)

        if col_name is None:
            raise ValueError("Invalid or missing column")

        pascal_case = r"'^[A-Z][a-z]+(?:[A-Z][a-z]+)*$'"    

        rule_def = f"CASE WHEN {col_name} RLIKE {pascal_case} THEN NULL ELSE '{col_name} is not in Pascal Case' END"

        return_val = {
            "rule_col_name": self._get_rule_col_name(col_name),
            "rule_def": rule_def
        }

        return self._rule_applies_to, return_val



"""
A class that checks if the values in a specified column are alphanumeric.

This class inherits from ObserveXRowRuleBase and provides functionality
to generate a rule for ensuring that the values in a specified column
contain only alphanumeric characters. It raises a ValueError if the column
name is missing or invalid.
"""

class ObserveColumnForAlphaNumericValues(ObserveXRowRuleBase):

    def __init__(self):
        """
        Initializes the ObserveColumnForAlphaNumericValues class by calling the constructor of 
        its superclass, ObserveXRowRuleBase.
        """
        super().__init__()

    def observation_rule(self, **kwargs):
        """
        Generates a SQL rule to check if the values in a specified column contain only
        alphanumeric characters.

        """
        col_name = kwargs.get('col_name', None)

        if col_name is None:
            raise ValueError("Invalid or missing column name")

        alpha_numeric = r"'^[a-zA-Z0-9]+$'"

        rule_def = f"CASE WHEN {col_name} RLIKE {alpha_numeric} THEN NULL ELSE '{col_name} does not contain alphanumeric values' END"
        return_val = {
            "rule_col_name": self._get_rule_col_name(col_name),
            "rule_def": rule_def
        }
        return self._rule_applies_to, return_val
