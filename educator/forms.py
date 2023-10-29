from django import forms
from educator.models import StudyGroup


class StudyGroupForm(forms.ModelForm):
    class Meta:
        model = StudyGroup
        fields = ['name', 'join_code', 'practice_goal']  # Add other fields if necessary
