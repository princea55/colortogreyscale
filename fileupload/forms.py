from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from django.forms import widgets
from django.core.exceptions import ValidationError


class FileUploadForm(forms.Form):
    file = forms.FileField()

    class Meta:
        fields = ['file']

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get("file")
        if not file:
            raise ValidationError('Please upload file.')
