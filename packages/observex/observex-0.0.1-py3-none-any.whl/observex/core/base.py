"""
This module contains the base class for the ObserveX library, as well as any enumerations needed.

The `ObserveXGlobalBase` class provides foundational functionality for the ObserveX library,
including base methods and attributes common to all parts of the library. Enumerations that 
are used throughout the library should also be defined in this module.
"""

import logging

class ObserveXGlobalBase(object):
    """
    Base class for the ObserveX library, providing foundational methods and attributes.

    This class is designed to be a base class for various components within the ObserveX library.
    It provides common methods and attributes, such as logging capabilities, that are intended to
    be used by other classes in the library.

    Attributes:
        logger (logging.Logger): A logger instance configured for the ObserveX library. By default,
                                  it is set to the ERROR logging level.

    Methods:
        __init__(self):
            Initializes the ObserveXGlobalBase with a logger instance set to the ERROR level.
    """
    def __init__(self):
        """
        Initializes the ObserveXGlobalBase with a logger instance.

        The logger is configured to use the module's name and is set to the
        ERROR logging level by default.
        This allows derived classes and other parts of the library to use the logger 
        for error reporting and debugging.
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.ERROR)
        super().__init__()
