"""File forms."""
from django import forms
from django.conf import settings
from django.core import validators


class UploadForm(forms.Form):
    """Upload form."""

    file = forms.FileField(
        validators=[
            validators.FileExtensionValidator(
                allowed_extensions=settings.MEDIA_ALLOWED_EXTENSIONS
            ),
        ]
    )
