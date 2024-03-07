from colorfield.widgets import ColorWidget
from django import forms
from .models import UserInfo, WeightObservation, WeightTarget

class UserInfoForm(forms.ModelForm):

    class Meta:
        model = UserInfo
        fields = ['baseline_weight']

class WeightObservationForm(forms.ModelForm):
    
    update_baseline = forms.BooleanField(
        label = 'Update Baseline',
        required = False,
    )
    class Meta:
        model = WeightObservation
        fields = ['value']
        
class WeightTargetForm(forms.ModelForm):
    
    class Meta:
        model = WeightTarget
        fields = ['name', 'value', 'colour']
        widgets = {
            'colour': ColorWidget(),
        }