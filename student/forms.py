from django import forms
from .models import UploadedText, UploadedFile, JoinGroup


class TextUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedText
        fields = ['content']


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']


class JoinGroupForm(forms.ModelForm):
    class Meta:
        model = JoinGroup
        fields = ['join_code']
