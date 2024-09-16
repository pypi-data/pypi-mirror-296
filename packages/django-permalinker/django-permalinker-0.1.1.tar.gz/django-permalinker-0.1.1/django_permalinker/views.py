"""
views.py: Views for django_permalinker.

This module defines the views for the django_permalinker application. It handles
the redirect functionality, which fetches a `Link` object by its ID and redirects
the user to the corresponding destination URL.
"""

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import Link


def redirect(request, link_id):  # pylint: disable=unused-argument
    """
    Redirect to the destination URL of the given link.

    This view retrieves the `Link` object associated with the provided `link_id`.
    If the `Link` is found, the user is redirected to its `destination_url`.
    If the `Link` does not exist, a 404 error is automatically raised.

    Args:
        request: The HTTP request object (unused in this view).
        link_id: The ID of the `Link` to retrieve and redirect to.

    Returns:
        HttpResponseRedirect: A redirect response to the link's destination URL.
    """

    # Fetch the Link object by its ID. If no Link with the given ID is found, a 404 error
    # is raised.
    link = get_object_or_404(Link, id=link_id)

    # Redirect the user to the destination URL of the retrieved Link object.
    return HttpResponseRedirect(link.destination_url)
