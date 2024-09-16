"""
apps.py: App config for django_permalinker.

This module defines the configuration for the django_permalinker application. It uses 
Django's AppConfig class to set up app-specific attributes, such as the name, label, 
and default auto field for model primary keys.
"""

from django.apps import AppConfig


class DjangoPermalinkerConfig(AppConfig):
    """
    Configuration class for the django_permalinker app.

    This class specifies app-specific settings, such as the default primary key field type,
    the app's internal name, label, and its human-readable name for the admin interface.
    """

    # Specifies the default field type for auto-incrementing primary keys.
    # By default, 'BigAutoField' is used, which is an integer field.
    default_auto_field = "django.db.models.BigAutoField"

    # The full Python path to the application (used by Django internally).
    name = "django_permalinker"

    # A short, unique label for the app, used in Django's internals to refer to the app.
    label = "permalinker"

    # A human-readable name for the app, which will be displayed in the Django admin interface.
    verbose_name = "Permalinker"
