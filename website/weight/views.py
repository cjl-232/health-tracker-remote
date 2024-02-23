from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from .forms import UserInfoForm, WeightObservationForm, WeightTargetForm
from .models import UserInfo, WeightObservation, WeightTarget

#Add an extra form for removing observations! Very important
#This should probably be another page...

#LAST THING NEEDED IS A STARTING POINT AND A BMI CALCULATOR, MAYBE ALSO HEIGHT

@login_required
def index_view(request):

    #Redirect users not yet registered with this app:
    if not UserInfo.objects.filter(user_id = request.user.id).exists():
        return redirect('weight:setup')

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
            'colour',
        ),
        columns = ['id', 'email', 'name', 'value', 'colour'],
    )
    
    #Set up user-specific querysets:
    user_info = UserInfo.objects.get(
        user_id = request.user.id
    )
    observations = WeightObservation.objects.filter(
        user_id = request.user.id,
    ).order_by(
        'datetime',
    )
    targets = WeightTarget.objects.filter(
        user_id = request.user.id,
    )
    
    #Determine progress values, formatted as percentages, from these:
    progress_values = {}
    for target in targets:
        if target.value != user_info.baseline_weight:
            change = user_info.baseline_weight - observations.last().weight
            target_change = user_info.baseline_weight - target.value
            progress = target_change / change
        else:
            progress = 1.0
        progress_values[target.name] = '{:.1%}'.format(np.clip(progress, 0, 1))

            
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
    
    fig = go.Figure()
    for target in targets:
        fig.add_hline(
            y = target.value,
            name = target.name,
            line_color = target.colour,
            line_dash = 'dash',
            showlegend = True,
        )
    df = pd.DataFrame(observations.values_list('datetime', 'weight'))
    fig.add_trace(
        go.Scatter(
            x = df[0],
            y = df[1],
            mode = 'lines+markers',
            name = 'Weight History',
            showlegend = True,
            legendrank = 999,
        )
    )
    weight_values = list(observations.values_list('weight', flat = True))
    target_values = list(targets.values_list('value', flat = True))
    fig.update_yaxes(
        range = [0, float(max(weight_values + target_values)) * 1.1],
        fixedrange = True,
    )
    
    
    
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

@login_required
def setup_view(request):
    #Redirect users with details already in place or successfully added:
    if UserInfo.objects.filter(user_id = request.user.id).exists():
        return redirect('weight:index')
        
    #Otherwise prepare a context dictionary:
    context = {}
        
    #If this is a POST request retrieve the form, otherwise create a new one:
    if request.method == 'POST':
        form = UserInfoForm(request.POST)
        context['user_info_form'] = form
        if form.is_valid():
            obj = form.save(commit = False)
            obj.user_id = request.user.id
            obj.save()
            WeightObservation.objects.create(
                user_id = obj.user_id,
                weight = obj.baseline_weight,
            )
            return redirect('weight:index')
        else:
            context['error_message'] = 'Invalid values supplied.'
    else:
        context['user_info_form'] = UserInfoForm()
    
    #Render the page with the provided context:
    return render(request, 'weight/setup.html', context = context)