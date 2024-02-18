from django import forms
from .models import WeightObservation, WeightTarget

class WeightObservationForm(forms.ModelForm):
    
    class Meta:
        model = WeightObservation
        fields = ['weight']
        
class WeightTargetForm(forms.ModelForm):
    
    class Meta:
        model = WeightTarget
        fields = ['name', 'value']