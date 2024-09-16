"""
settings.py: Customizable settings for django_permalinker.

This module defines settings specific to the django_permalinker application.
These settings allow control over how permalink IDs are generated, including
the length of the IDs, whether uppercase or lowercase characters are used, 
and whether digits are included in the ID generation.
"""

from django.conf import settings

# The default length of the generated permalink ID (default: 5).
# This can be overridden by defining PERMALINKER_ID_LENGTH in the Django project's settings.
PERMALINKER_ID_LENGTH: int = getattr(settings, "PERMALINKER_ID_LENGTH", 5)

# Specifies whether the generated ID should include uppercase letters.
# Defaults to True, meaning the generated ID will include both lowercase and uppercase letters
# unless this setting is overridden to False.
PERMALINKER_ID_INCLUDE_UPPERCASE: bool = getattr(settings, "PERMALINKER_ID_INCLUDE_UPPERCASE", True)

# Specifies whether digits (1-9) should be included in the generated ID.
# Defaults to True, meaning the generated ID will include both letters and numbers unless
# overridden.
PERMALINKER_ID_INCLUDE_DIGITS: bool = getattr(settings, "PERMALINKER_ID_INCLUDE_DIGITS", True)
