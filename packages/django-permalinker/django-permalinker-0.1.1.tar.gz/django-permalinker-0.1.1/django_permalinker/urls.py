"""
urls.py: URL configurations for the django_permalinker app.

This module defines the URL patterns for the django_permalinker app. It includes a
single URL pattern that captures a link ID and maps it to the corresponding redirect view.
"""

from django.urls import path
from . import views

# Set the app namespace for the django_permalinker app, used for namespacing URLs in templates.
app_name = "permalinker"  # pylint: disable=invalid-name

# URL patterns for the app.
urlpatterns = [
    # Matches any string as the link ID and maps it to the 'redirect' view.
    # Example: /abc123/ will redirect to the destination URL of the link with ID 'abc123'.
    path("<str:link_id>/", views.redirect, name="redirect"),
]
