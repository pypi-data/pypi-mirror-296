"""
This module contains classes for executing observation rules within the ObserveX library.

The classes defined in this module are responsible for applying various observation rules to 
datasets. These classes are designed to handle observations at different levels, such as rows, 
columns, datasets, and metadata.

"""
from pyspark.sql import functions as F
from observex.core.base import ObserveXGlobalBase as oxb
from observex.observers.rowobservers import *
from observex.observers.columnobservers import *
from observex.core.utils import *

class ObservationExecutorBase(oxb.ObserveXGlobalBase):
    """
    Base class for executing observation rules in the ObserveX library.

    This abstract class defines the interface for executing observation rules. Subclasses must 
    implement the `execute_observations` method to apply rules to a dataset.

    Methods:
    - execute_observations(dataset, ruleset): Abstract method to execute observations.
    """
    def __init__(self):
        """
        Initializes the ObservationExecutorBase class.
        """
        oxb.logging.debug("Initializes the ObservationExecutorBase class.")
        super().__init__()

    def execute_observations(self, dataset, ruleset):
        """
        Abstract method to execute observations on the dataset based on the ruleset.

        Subclasses must implement this method to apply the provided ruleset to the dataset.

        Parameters:
        - dataset: The dataset on which observations will be applied.
        - ruleset: A list of rules to be applied to the dataset.

        Raises:
        - NotImplementedError: If not implemented in the subclass.
        """
        oxb.logging.error("Not implemented in base-class. Must be implemented in sub-class")
        raise NotImplementedError("Not implemented in base-class. Must be implemented in sub-class")

class ObservationExecutorFactory(oxb.ObserveXGlobalBase):
    """
    Factory class for creating instances of observation executors.

    This class provides a method to obtain instances of observation executor classes by name. 
    It validates if the class exists and if it is a subclass of `ObservationExecutorBase`.

    Methods:
    - get_instance(name): Retrieves an instance of an observation executor class by name.
    """
    def __init__(self):
        """
        Initializes the ObservationExecutorFactory class.
        """
        oxb.logging.debug("Initializes the ObservationExecutorFactory class.")
        super().__init__()
    
    def get_instance(self, rule_type):
        """
        Retrieves an instance of the observation executor class based on the rule_type ('row', 'column', etc.).

        Parameters:
        - rule_type (str): The type of rule ('row', 'column', etc.).

        Returns:
        - An instance of the appropriate observation executor class.

        Raises:
        - ValueError: If the rule_type is not recognized.
        """
        # Map rule types to corresponding executor class names
        class_map = {
            'row': 'RowObservationExecutor',
            'column': 'ColumnObservationExecutor'
        }

        if rule_type in class_map:
            class_name = class_map[rule_type]
            if class_name in globals():
                obj = globals()[class_name]
                if issubclass(obj, ObservationExecutorBase):
                    return obj()
                else:
                    raise NotImplementedError(f"[{class_name}] is not implemented.")
            else:
                raise NameError(f"[{class_name}] is not found in global context.")
        else:
            raise ValueError(f"Unknown rule type: {rule_type}")
        

class ObserveXExecutor(oxb.ObserveXGlobalBase):
    """
    Main executor for applying observation rules on different aspects of a dataset.

    This class manages the execution of observation rules on rows, columns, datasets, and metadata. 
    It uses the `ObservationExecutorFactory` to create instances of specific executors based on the 
    ruleset.

    Methods:
    - execute(dataset, ruleset, separate_columns=False): Executes observation rules on the dataset 
      and returns the results.
    """
    def __init__(self):
        """
        Initializes the ObserveXExecutor class.
        """
        oxb.logging.debug("Initializes the ObserveXExecutor class.")
        super().__init__()

    def execute(self, dataset, ruleset, separate_columns=False):
        oxb.logging.debug("Parsing ruleset for row and column rules")

        # Split the ruleset into row rules and column rules
        row_rules = [rule for rule in ruleset if "row" in rule.get("rule_type").lower()]
        column_rules = [rule for rule in ruleset if "column" in rule.get("rule_type").lower()]

        # Initialize results for row and column observations
        observed_rows, observed_columns = None, None

        # Execute row observations if row rules exist
        if row_rules:
            row_observer = ObservationExecutorFactory().get_instance("row")
            oxb.logging.debug("Executing row rules using RowObservationExecutor")
            observed_rows = row_observer.execute_observations(dataset, row_rules, separate_columns)

        # Execute column observations if column rules exist
        if column_rules:
            column_observer = ObservationExecutorFactory().get_instance("column")
            oxb.logging.debug("Executing column rules using ColumnObservationExecutor")
            observed_columns = column_observer.execute_observations(dataset, column_rules)

        return {
            "row_observations": observed_rows,
            "column_observations": observed_columns
        }




class RowObservationExecutor(ObservationExecutorBase):
    """
    Executor for applying row-specific observation rules on a dataset.

    This class implements the `execute_observations` method to handle row-specific observations 
    based on the provided ruleset.

    Methods:
    - execute_observations(dataset, ruleset, separate_columns=False): 
    Applies row-specific observation rules.
    """
    def __init__(self):
        """
        Initializes the RowObservationExecutor class.
        """
        oxb.logging.debug("Initializes the RowObservationExecutor class.")
        super().__init__()

    def execute_observations(self, dataset, ruleset, separate_columns=False):
        """
        Applies row-specific observation rules to the dataset.

        This method initializes a column for storing validation information and applies each 
        rule from the ruleset. It populates the `_observex_validation_info` column with details 
        of failed observations.

        Parameters:
        - dataset: The dataset on which row observations will be applied.
        - ruleset: A list of row-specific rules to be applied to the dataset.
        - separate_columns: A flag to determine if validation information 
        should be shown in separate columns.

        Returns:
        - A tuple containing:
          - A DataFrame with valid rows (where `__ox_is_valid` is True).
          - A DataFrame with all rows and validation information.
          - A DataFrame with summary validation information.
        """
        oxb.logging.debug(f"Executing observation for Row Rules with separate_columns = {separate_columns}")
        df_with_ox_cols = dataset.withColumn("__ox_observex_validation_info", F.array())
        df_with_ox_cols = df_with_ox_cols.withColumn("__ox_is_valid", F.lit(True))

        if separate_columns:
            df_with_ox_cols = df_with_ox_cols.drop("__ox_observex_validation_info")

        for rule in ruleset:
            rule_args = {}
            orule = ObserveXRowRuleFactory().get_instance(rule["observe"])
            for key, val in rule.items():
                if key != "observe":
                    rule_args[key] = val

            rule_applies_to, rule_output = orule.observation_rule(**rule_args)

            if rule_applies_to == "row":
                rule_def = rule_output["rule_def"]
                rule_col_name = f"__ox_{rule['observe']}".replace(" ", "_")
                sev_level = rule.get("sev_level", "error").lower()
                if separate_columns:
                    df_with_ox_cols = df_with_ox_cols.withColumn(
                        rule_col_name,
                        F.expr(f"CASE WHEN {rule_def} IS NOT NULL THEN {rule_def} ELSE NULL END")
                    )
                else:
                    df_with_ox_cols = df_with_ox_cols.withColumn(
                        "__ox_observex_validation_info",
                        F.expr(f"""
                            filter(
                                array_union(
                                    __ox_observex_validation_info,
                                    array(
                                        CASE WHEN {rule_def} IS NOT NULL THEN 
                                            named_struct(
                                                'failed_field', '{rule_col_name}',
                                                'failed_value', {rule_def},
                                                'sev_level', '{sev_level}',
                                                'observation_rule', '{rule["observe"]}'
                                            )
                                        ELSE NULL END
                                    )
                                ),
                                x -> x IS NOT NULL
                            )
                        """)
                    )
                if sev_level == "error":
                    df_with_ox_cols = df_with_ox_cols.withColumn(
                        "__ox_is_valid",
                        F.when(F.expr(f"{rule_def} IS NOT NULL"), F.lit(False)).otherwise(df_with_ox_cols["__ox_is_valid"])
                    )    
        df_valid_rows = df_with_ox_cols.filter(df_with_ox_cols["__ox_is_valid"] == True)
        df_df_with_ox_cols_raw = df_with_ox_cols
        all_cols = dataset.columns
        if "__ox_observex_validation_info" in df_with_ox_cols.columns:
            df_df_with_ox_cols_summary = df_with_ox_cols
        else:
            oxb.logging.debug("Rebuilding the __ox_observex_validation_info column for summary.")
            rule_columns = [col for col in df_with_ox_cols.columns if col.startswith("__ox_") and col != "__ox_is_valid"]
            df_df_with_ox_cols_summary = df_with_ox_cols.withColumn(
                "__ox_observex_validation_info",
                F.array(*[F.struct(F.lit(col).alias('failed_field'), F.col(col).alias('failed_value')) for col in rule_columns])
            ).select(*all_cols, "__ox_observex_validation_info", "__ox_is_valid")
        if separate_columns:
            df_valid_rows = df_valid_rows.drop("__ox_observex_validation_info")
            df_df_with_ox_cols_raw = df_df_with_ox_cols_raw.drop("__ox_observex_validation_info")
        ox_row_rules_result = [df_valid_rows, df_df_with_ox_cols_raw, df_df_with_ox_cols_summary]
        return ox_row_rules_result

class ColumnObservationExecutor(ObservationExecutorBase):
    """
    Executor for applying column-specific observation rules on a dataset.

    This class implements the `execute_observations` method to handle column-specific observations 
    based on the provided ruleset.

    Methods:
    - execute_observations(dataset, ruleset): Applies column-specific observation rules.
    """
    def __init__(self):
        """
        Initializes the ColumnObservationExecutor class.
        """
        oxb.logging.debug("Initializes the ColumnObservationExecutor class.")
        super().__init__()

    def execute_observations(self, dataset, ruleset):
        """
        Applies column-specific observation rules to the dataset.

        This method aggregates results based on the ruleset and prepares data for tabulation.

        Parameters:
        - dataset: The dataset on which column observations will be applied.
        - ruleset: A list of column-specific rules to be applied to the dataset.

        Returns:
        - A DataFrame containing the results of column observations, formatted for display.
        """
        results = {}

        columns = sorted(set(rule["col_name"] for rule in ruleset))
        rules = sorted(set(rule["observe"] for rule in ruleset))

        for rule in rules:
            results[rule] = {col: None for col in columns}

        for rule in ruleset:
            rule_name = rule["observe"]
            col_name = rule["col_name"]

            rule_args = {key: val for key, val in rule.items() if key != "observe"}
            orule = ObserveXColumnRuleFactory().get_instance(rule_name)
            rule_applies_to, rule_output = orule.observation_rule(**rule_args)

            if rule_applies_to == "column":
                rule_def = rule_output["rule_def"]
                validation_result = dataset.agg(F.expr(rule_def)).collect()[0][0]

                # Store the result in the dictionary
                results[rule_name][col_name] = str(validation_result)

        table_data = []
        for rule in rules:
            row = [rule] + [results[rule].get(col, 'N/A') for col in columns]
            table_data.append(row)

        headers = ["Rules"] + columns
        df_with_ox_cols = ObserveXInternalUtils.convert_dict_to_df(self, table_data, headers)
        return df_with_ox_cols

class DatasetObservationExecutor(ObservationExecutorBase):
    """
    Base class for executing dataset-specific observation rules.

    This class is intended to be subclassed to implement dataset-specific observation logic.

    Methods:
    - execute_observations(dataset, ruleset): Abstract method to execute dataset observations.
    """
    def __init__(self):
        """
        Initializes the DatasetObservationExecutor class.
        """
        oxb.logging.debug("Initializes the DatasetObservationExecutor class.")
        super().__init__()

    def execute_observations(self, ds, rs):
        """
        Abstract method for executing dataset-specific observation rules.

        Parameters:
        - ds: The dataset on which dataset observations will be applied.
        - rs: A list of dataset-specific rules to be applied to the dataset.

        Raises:
        - NotImplementedError: If not implemented in the subclass.
        """
        oxb.logging.error("Not implemented yet in sub-class.")
        raise NotImplementedError("Not implemented yet in sub-class.")

class MetadataObservationExecutor(ObservationExecutorBase):
    """
    Base class for executing metadata-specific observation rules.

    This class is intended to be subclassed to implement metadata-specific observation logic.

    Methods:
    - execute_observations(dataset, ruleset): Abstract method to execute metadata observations.
    """
    def __init__(self):
        """
        Initializes the MetadataObservationExecutor class.
        """
        oxb.logging.debug("Initializes the MetadataObservationExecutor class.")
        super().__init__()

    def execute_observations(self, ds, rs):
        """
        Abstract method for executing metadata-specific observation rules.

        Parameters:
        - ds: The dataset on which metadata observations will be applied.
        - rs: A list of metadata-specific rules to be applied to the dataset.

        Raises:
        - NotImplementedError: If not implemented in the subclass.
        """
        oxb.logging.error("Not implemented yet in sub-class.")
        raise NotImplementedError("Not implemented yet in sub-class.")
