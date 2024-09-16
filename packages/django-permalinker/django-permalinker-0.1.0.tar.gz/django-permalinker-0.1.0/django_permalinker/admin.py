"""
admin.py: Admin classes for django_permalinker.

This module defines the Django admin interface for the Link model. It customizes
the way Link objects are displayed, searched, filtered, and edited within the admin.
"""

from django.contrib import admin
from .models import Link


class LinkAdmin(admin.ModelAdmin):
    """
    Admin interface for the Link model.

    This class defines how Link objects are displayed and managed in the Django admin panel.
    It customizes the list display, search fields, filters, and readonly fields, allowing
    administrators to manage links efficiently.
    """

    # Specifies the fields to display in the admin list view.
    # The 'name' is the link's name, and 'destination_url_html' renders the clickable destination
    # URL.
    list_display = ["name", "destination_url_html"]

    # Fields that can be searched within the admin interface. This includes the name of the link,
    # the destination URL, the link ID.
    search_fields = ["name", "destination_url", "id"]

    # Fields that allow filtering of link entries based on their creation and modification dates.
    list_filter = ["created_at", "modified_at"]

    # Specifies the default ordering of links in the list view, which is by name.
    ordering = ["name"]

    # Fields that are displayed when viewing or editing a single Link object.
    # Some fields are rendered as read-only, such as 'permanent_url_html', 'created_at', and
    # 'modified_at'.
    fields = [
        "permanent_url_html", "destination_url", "name", "description", "created_at",
        "modified_at"
    ]

    # Specifies fields that are read-only and cannot be edited by administrators.
    # 'permanent_url_html' displays the permanent URL, while 'created_at' and 'modified_at' are
    # timestamps.
    readonly_fields = ["permanent_url_html", "created_at", "modified_at"]


# Registers the Link model with the admin site, using the LinkAdmin configuration.
admin.site.register(Link, LinkAdmin)
