from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
import pandas as pd

from .forms import WeightObservationForm, WeightTargetForm
from .models import WeightObservation, WeightTarget

#Add an extra form for removing observations! Very important

@login_required
def index_view(request):

    weight_observation_form = WeightObservationForm()
    weight_observation_form_error = None
    weight_target_form = WeightTargetForm()
    weight_target_form_error = None
    
    if request.method == 'POST':
        if request.POST.get('form_name') == 'weight_observation_form':
            weight_observation_form = WeightObservationForm(request.POST)
            if weight_observation_form.is_valid():
                obj = weight_observation_form.save(commit = False)
                obj.user_id = request.user.id
                obj.save()
                return redirect('weight:index')
            else:
                weight_observation_form_error = 'Invalid entry.'
        elif request.POST.get('form_name') == 'weight_target_form':
            weight_target_form = WeightTargetForm(request.POST)
            if weight_target_form.is_valid():
                obj = weight_target_form.save(commit = False)
                obj.user_id = request.user.id
                obj.save()
                return redirect('weight:index')
            else:
                weight_target_form_error = 'Invalid entry.'
                
    weight_history = pd.DataFrame.from_records(
        WeightObservation.objects.filter(
            user_id = request.user.id,
        ).order_by(
            'datetime',
        ).values_list(
            'user_id__email',
            'weight',
            'datetime',
        )
    )
    weight_targets = pd.DataFrame.from_records(
        WeightTarget.objects.filter(
            user_id = request.user.id,
        ).values_list(
            'user_id__email',
            'name',
            'value',
        )
    )
    context = {
        'data': weight_history,
        'data2': weight_targets,
        'weight_observation_form': weight_observation_form,
        'weight_observation_form_error': weight_observation_form_error,
        'weight_target_form': weight_target_form,
        'weight_target_form_error': weight_target_form_error,
    }
    return render(request, 'weight/index.html', context = context)
