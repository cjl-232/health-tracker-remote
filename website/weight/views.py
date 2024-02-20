from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
import pandas as pd

from .forms import WeightObservationForm, WeightTargetForm
from .models import WeightObservation, WeightTarget

#Add an extra form for removing observations! Very important
#This should probably be another page...

@login_required
def index_view(request):

    weight_observation_form = WeightObservationForm()
    weight_observation_form_error = None
    weight_target_form = WeightTargetForm()
    weight_target_form_error = None
    
    if request.method == 'POST':
        if request.POST.get('form_name') == 'add_weight_observation_form':
            weight_observation_form = WeightObservationForm(request.POST)
            if weight_observation_form.is_valid():
                obj = weight_observation_form.save(commit = False)
                obj.user_id = request.user.id
                obj.save()
                return redirect('weight:index')
            else:
                weight_observation_form_error = 'Invalid entry.'
        elif request.POST.get('form_name') == 'del_weight_observation_form':
            id = int(request.POST.get('observation_choice'))
            WeightObservation.objects.get(id = id).delete()
        elif request.POST.get('form_name') == 'add_weight_target_form':
            weight_target_form = WeightTargetForm(request.POST)
            if weight_target_form.is_valid():
                obj = weight_target_form.save(commit = False)
                obj.user_id = request.user.id
                obj.save()
                return redirect('weight:index')
            else:
                weight_target_form_error = 'Invalid entry.'
        elif request.POST.get('form_name') == 'del_weight_target_form':
            id = int(request.POST.get('target_choice'))
            WeightTarget.objects.get(id = id).delete()

    weight_history = pd.DataFrame.from_records(
        WeightObservation.objects.filter(
            user_id = request.user.id,
        ).order_by(
            'datetime',
        ).values_list(
            'id',
            'user_id__email',
            'weight',
            'datetime',
        ),
        columns = ['id', 'email', 'weight', 'datetime'],
    )
    weight_targets = pd.DataFrame.from_records(
        WeightTarget.objects.filter(
            user_id = request.user.id,
        ).values_list(
            'id',
            'user_id__email',
            'name',
            'value',
        ),
        columns = ['id', 'email', 'name', 'value'],
    )
    
    #Retrieve lists of dictionaries to use in deletion dropdowns:
    recent_observations = None
    if not weight_history.empty:
        recent_observations = weight_history[-10:].iloc[::-1].apply(
            lambda row: {
                'id': row['id'],
                'label': ' - '.join([
                    row['datetime'].strftime('%Y/%m/%d'),
                    '{0:.1f}'.format(row['weight']) + 'kg',
                ]),
            },
            axis = 1,
        ).tolist()
    
    targets_list = None
    if not weight_targets.empty:
        targets_list = weight_targets.sort_values('name').apply(
            lambda row: {
                'id': row['id'],
                'label': ' - '.join([
                    row['name'],
                    '{0:.1f}'.format(row['value']) + 'kg',
                ]),
            },
            axis = 1,
        ).tolist()
    
    
    pd.options.plotting.backend = 'plotly'
    fig = weight_history.plot('datetime', 'weight')
    
    
    context = {
        'data': weight_history,
        'data2': weight_targets,
        'deletion_dropdown_lists': {
            'observations': recent_observations,
            'targets': targets_list,
        },
        'plot': fig.to_html(full_html = False, include_plotlyjs = 'cdn'),
        'weight_observation_form': weight_observation_form,
        'weight_observation_form_error': weight_observation_form_error,
        'weight_target_form': weight_target_form,
        'weight_target_form_error': weight_target_form_error,
    }
    return render(request, 'weight/index.html', context = context)
