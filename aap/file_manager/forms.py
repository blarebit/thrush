from django import forms
from django.core import validators
from django.conf import settings


class UploadFileForm(forms.Form):
    print("UploadFileForm")
    file = forms.FileField(
        validators=[
            validators.validate_image_file_extension,
            # validators.FileExtensionValidator(allowed_extensions=settings.MEDIA_ALLOWED_EXTENSIONS),
        ]
    )
