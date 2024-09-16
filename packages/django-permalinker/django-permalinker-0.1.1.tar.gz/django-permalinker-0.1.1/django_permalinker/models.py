"""
models.py: Models for django_permalinker.

This file defines the Link model used for generating and managing permalinks.
It includes logic for auto-generating unique IDs, URL representations, and admin display
functionality.
"""

import random

from django.db import models
from django.urls import reverse
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from . import settings
from .exceptions import NoUniqueIdError


class Link(models.Model):
    """
    Represents a permalink with a unique ID, pointing to a destination URL.

    Attributes:
        id (str): The unique auto-generated identifier for the link.
        destination_url (URLField): The destination URL the permalink redirects to.
        name (str): The name of the link.
        description (TextField): Optional description of the link.
        created_at (DateTimeField): The timestamp when the link was created.
        modified_at (DateTimeField): The timestamp when the link was last modified.
    """

    id = models.CharField(
        _("ID"), max_length=settings.PERMALINKER_ID_LENGTH, editable=False, primary_key=True
    )
    destination_url = models.URLField(_("Destination URL"))
    name = models.CharField(_("Name"), max_length=255, unique=True)
    description = models.TextField(_("Description"), null=True, blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified at"), auto_now=True)

    def __str__(self):
        """
        Returns the string representation of the link object.

        This is primarily used in the Django admin and other interfaces that display the object.
        """
        return self.name

    def get_absolute_url(self):
        """
        Generates the absolute URL for the permalink.

        Returns:
            str: The absolute URL for redirecting to the link based on its unique ID.
            None: If the link does not yet have an ID.
        """
        if self.id:
            return reverse("permalinker:redirect", args=(self.id,))
        return None

    @admin.display(description="Permanent URL", ordering="id")
    def permanent_url_html(self):
        """
        Generates an HTML link for the permanent URL in the admin panel.

        Returns:
            str: A clickable link to the permalink if an ID is available, or '-' otherwise.
        """
        url = self.get_absolute_url()
        if url:
            return mark_safe(f'<a href="{url}">{url}</a>')
        return "-"

    @admin.display(description=_("Destination URL"))
    def destination_url_html(self):
        """
        Generates an HTML link to the destination URL in the admin panel.

        Returns:
            str: A clickable link to the destination URL.
        """
        return mark_safe(f'<a href="{self.destination_url}">{self.destination_url}</a>')

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to automatically generate a unique ID if not provided.

        The ID is generated using a custom base58 character set (excluding ambiguous characters),
        with configurable options to include digits or uppercase letters.

        Raises:
            NoUniqueIdError: If no unique ID can be generated after the maximum number of attempts.
        """
        if not self.id:
            # Define the base58 character set for ID generation (excluding ambiguous characters
            # like 0, O, I, l)
            base58_chars = "abcdefghijkmnopqrstuvwxyz"
            # Include digits in the character set if allowed by settings
            if settings.PERMALINKER_ID_INCLUDE_DIGITS:
                base58_chars += "123456789"
            # Include uppercase letters if allowed by settings
            if settings.PERMALINKER_ID_INCLUDE_UPPERCASE:
                base58_chars += "ABCDEFGHJKLMNPQRSTUVWXYZ"
            id_length = settings.PERMALINKER_ID_LENGTH
            # Generate 10 candidate IDs at once
            ids = {
                "".join(random.choice(base58_chars) for _ in range(id_length)) for _ in range(10)
            }
            # Check if any of these IDs already exist in the database
            existing_ids = set(Link.objects.filter(id__in=ids).values_list("id", flat=True))
            # Find available IDs (those not already in use)
            available_ids = ids - existing_ids
            if available_ids:
                # If there is at least one available ID, use it
                self.id = available_ids.pop()
            else:
                # If no unique ID was found, raise an exception
                raise NoUniqueIdError(
                    "Couldn't generate a unique ID for the link. "
                    "Increase the value of PERMALINKER_ID_LENGTH in settings."
                )
        # Call the superclass save method to save the object to the database
        super().save(*args, **kwargs)

    class Meta:
        """Meta information for the Link model, including localization."""
        verbose_name = _("Link")
        verbose_name_plural = _("Links")
