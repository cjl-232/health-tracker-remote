from django import forms
from .models import UserInfo, WeightObservation, WeightTarget

class UserInfoForm(forms.ModelForm):

    class Meta:
        model = UserInfo
        fields = ['baseline_weight']

class WeightObservationForm(forms.ModelForm):
    
    class Meta:
        model = WeightObservation
        fields = ['weight']
        
class WeightTargetForm(forms.ModelForm):
    
    class Meta:
        model = WeightTarget
        fields = ['name', 'value']