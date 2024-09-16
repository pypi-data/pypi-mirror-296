"""
exceptions.py: Custom exception classes for django_permalinker.

This module defines custom exceptions used within the django_permalinker app.
"""


class NoUniqueIdError(Exception):
    """
    Exception raised when no unique ID could be generated.

    This error is raised when the application fails to generate a unique ID for a model 
    object. This typically happens when the ID space is too small or when there are many
    existing records that consume most available unique IDs.
    """
