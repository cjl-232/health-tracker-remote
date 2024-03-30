from django import forms
from django.forms.widgets import TextInput
from .models import ComponentDefinition

class ComponentDefinitionForm(forms.ModelForm):

    class Meta:
        model = ComponentDefinition
        fields = ['name', 'groups']