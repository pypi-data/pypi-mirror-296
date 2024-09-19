# exceptions.py
"""
    A hybrid approach, where common exceptions are predefined and the dynamic creation is used for module-specific
    exceptions. The ExceptionFactory inherits from OxExceptionBase.
This module defines the core exception classes for the ObserveX library.

All exceptions in the ObserveX library will inherit from these base classes.
"""


# Define a base custom exception
class OxExceptionBase(Exception):
    """
    Base class for all exceptions in the ObserveX library.

    This class is the foundation for defining custom exceptions within the ObserveX library.
    It provides a default error message and can be used to catch 
    any exceptions that are specific to the ObserveX library.

    Attributes:
        message (str): The error message associated with the exception.

    Methods:
        __init__(self, message="ObserveX error."):
            Initializes the OxExceptionBase with a custom or default error message.
        __str__(self):
            Returns the error message string for the exception.
    """
    def __init__(self, message="ObserveX error."):
        """
        Initializes the OxExceptionBase with a custom or default error message.

        Args:
            message (str): The error message to be associated with this exception. 
            Defaults to "ObserveX error."
        
        This method also logs the initialization process for debugging purposes.
        """
        super().__init__(message)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the error message.

        Returns:
            str: The error message associated with this exception.
        """
        return self.message
    """Base class for all custom exceptions"""
    pass

# Exception factory for dynamically creating module-specific exceptions
class ExceptionFactory(OxExceptionBase):
    @staticmethod
    def create_exception(name, base_exception=OxExceptionBase):
        return type(name, (base_exception,), {})

def create_exception(name, base_exception=OxExceptionBase):
    return ExceptionFactory.create_exception(name, base_exception)

# Predefined exceptions (Hierarchy)
class ValidationError(OxExceptionBase):
    """Raised when a validation error occurs"""
    pass

class DatabaseError(OxExceptionBase):
    """Raised when there is a database-related error"""
    pass

class ConnectionError(DatabaseError):
    """Raised when there is a connection issue"""
    pass

class TransactionError(DatabaseError):
    """Raised when there is a transaction-related issue"""
    pass

class FileError(OxExceptionBase):
    """Raised when a file-related error occurs"""
    pass

class FileNotFoundError(FileError):
    """Raised when a file is not found"""
    pass

class ObserverError(OxExceptionBase):
    """Base class for observer-related errors."""
    pass

class RowObserverError(ObserverError):
    """Base class for row observer-related errors."""
    pass

class RowRuleFactoryError(RowObserverError):
    """Raised when there's an issue with the ObserveXRowRuleFactory."""
    pass

class RowRuleNotFoundError(RowRuleFactoryError):
    """Raised when a requested row rule is not found or not implemented."""
    pass

class InvalidRowRuleParameterError(RowObserverError):
    """Raised when invalid parameters are provided to a row rule."""
    pass

""" Specific exceptions for each row observer class """

class ColumnLengthBetweenError(RowObserverError):
    """Raised for issues in ObserveColumnLengthBetween."""
    pass

class MultiFieldSumToEqualError(RowObserverError):
    """Raised for issues in ObserveMultiFieldSumToEqual."""
    pass

class FieldValueBetweenError(RowObserverError):
    """Raised for issues in ObserveFieldValueBetween."""
    pass

class SetExpectationError(RowObserverError):
    """Raised for issues in ObserveSetExpectation."""
    pass

class ColumnValueForEmailError(RowObserverError):
    """Raised for issues in ObserveColumnValueForEmail."""
    pass

class ColumnValueForUuidError(RowObserverError):
    """Raised for issues in ObserveColumnValueForUuid."""
    pass

class ColumnValueForPatternError(RowObserverError):
    """Raised for issues in ObserveColumnValueForPattern."""
    pass

class ColumnForNullValueError(RowObserverError):
    """Raised for issues in ObserveColumnForNullValue."""
    pass

class ColumnForSetValuesError(RowObserverError):
    """Raised for issues in ObserveColumnForSetValues."""
    pass

class ColumnForDomainValuesError(RowObserverError):
    """Raised for issues in ObserveColumnForDomainValues."""
    pass

class ColumnValueForCamelcaseError(RowObserverError):
    """Raised for issues in ObserveColumnValueForCamelcase."""
    pass

class ColumnValueForLowercaseError(RowObserverError):
    """Raised for issues in ObserveColumnValueForLowercase."""
    pass

class ColumnValueForUppercaseError(RowObserverError):
    """Raised for issues in ObserveColumnValueForUppercase."""
    pass

class UniquenessCheckError(RowObserverError):
    """Raised for issues in ObserveUniquenessCheck."""
    pass

class SpecialCharacterCheckError(RowObserverError):
    """Raised for issues in ObserveSpecialCharacterCheck."""
    pass

class ColumnMinLengthError(RowObserverError):
    """Raised for issues in ObserveColumnMinLength."""
    pass

class ColumnMaxLengthError(RowObserverError):
    """Raised for issues in ObserveColumnMaxLength."""
    pass

class ColumnValueForKebabcaseError(RowObserverError):
    """Raised for issues in ObserveColumnValueForKebabcase."""
    pass

class ColumnValueForSnakecaseError(RowObserverError):
    """Raised for issues in ObserveColumnValueForSnakecase."""
    pass

class ColumnValueForPascalcaseError(RowObserverError):
    """Raised for issues in ObserveColumnValueForPascalcase."""
    pass

class ColumnForAlphaNumericValuesError(RowObserverError):
    """Raised for issues in ObserveColumnForAlphaNumericValues."""
    pass

# Additional general exceptions
class InvalidDatasetError(OxExceptionBase):
    """
    Exception raised when a dataset is invalid.

    This exception inherits from OxExceptionBase and is used to indicate 
    errors related to invalid datasets.
    """
    pass

class InvalidRulesetError(OxExceptionBase):
    """Raised when a ruleset is invalid or cannot be applied."""
    pass

class RuleApplicationError(OxExceptionBase):
    """Raised when there's an error applying a rule to data."""
    pass

class DataSourceError(OxExceptionBase):
    """Raised when there's an issue with the data source."""
    pass

class ValidationError(OxExceptionBase):
    """Raised when data validation fails."""
    pass

class TransformationError(OxExceptionBase):
    """Raised when there's an error during data transformation."""
    pass

class ExecutorError(OxExceptionBase):
    """Raised when there's an issue with executors."""
    pass

class IntegrationError(OxExceptionBase):
    """Base class for integration-related errors."""
    pass

class ConfigurationError(OxExceptionBase):
    """Raised when there's a configuration-related issue."""
    pass

class PerformanceError(OxExceptionBase):
    """Raised when there's a performance-related issue."""
    pass
    """
    Exception raised when a ruleset is invalid.

    This exception inherits from OxExceptionBase and is used to indicate errors 
    related to invalid rulesets.
    """
    pass
