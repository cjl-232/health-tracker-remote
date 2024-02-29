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
        
    #Prepare a context dictionary:
    context = {
        'observation_form': WeightObservationForm(),
        'target_form': WeightTargetForm(),
    }
    
    #If this is a post request, determine the submitted form and handle it:
    if request.method == 'POST':
        match request.POST.get('form_name'):
            case 'add_observation':
                form = WeightObservationForm(request.POST)
                if form.is_valid():
                    obj = form.save(commit = False)
                    obj.user_id = request.user.id
                    obj.save()
                else:
                    context['observation_form'] = form
            case 'add_target':
                form = WeightTargetForm(request.POST)
                if form.is_valid():
                    obj = form.save(commit = False)
                    obj.user_id = request.user.id
                    obj.save()
                else:
                    context['target_form'] = form
            case 'delete_observation':
                id = int(request.POST.get('choice'))
                object = WeightObservation.objects.get(pk = id)
                if object.user_id == request.user.id:
                    object.delete()
            case 'delete_target':
                id = int(request.POST.get('choice'))
                object = WeightTarget.objects.get(pk = id)
                if object.user_id == request.user.id:
                    object.delete()

    #Set up user-specific querysets:
    user_info = UserInfo.objects.get(
        user_id = request.user.id
    )
    observations = WeightObservation.objects.filter(
        user_id = request.user.id,
    ).order_by(
        '-datetime',
    )
    targets = WeightTarget.objects.filter(
        user_id = request.user.id,
    ).order_by(
        '-value',
    )
    
    #Produce observation-related text to pass as context:
    context['recent_observation_details'] = []
    for observation in observations[:10]:
        context['recent_observation_details'].append({
            'id': observation.id,
            'label': str(observation),
        })
    
    #Produce target-related text to pass as context:
    if targets.exists:
        context['target_details'] = []
        def make_target_dict(target, baseline_weight, current_weight):
            if target.value != baseline_weight:
                actual_decrease = baseline_weight - current_weight
                target_decrease = baseline_weight - target.value
                progress = np.clip(actual_decrease / target_decrease, 0.0, 1.0)
            else:
                progress = 1.0
            return {
                'id': target.id,
                'label': str(target),
                'progress': '{:.1%}'.format(progress),
            }
        for target in targets:
            context['target_details'].append(
                make_target_dict(
                    target,
                    user_info.baseline_weight,
                    observations[1].value,
                )
            )
    
    #Produce a plot to pass as context:
    time_series_df = pd.DataFrame(
        observations.values_list('datetime', 'value'),
    )
    fig = go.Figure()
    for target in targets:
        fig.add_hline(
            y = target.value,
            name = target.name,
            line_color = target.colour,
            line_dash = 'dash',
            showlegend = True,
        )
    fig.add_trace(
        go.Scatter(
            x = time_series_df[0],
            y = time_series_df[1],
            mode = 'lines+markers',
            name = 'Weight History',
            showlegend = True,
            legendrank = 999,
        )
    )
    weight_values = list(observations.values_list('value', flat = True))
    target_values = list(targets.values_list('value', flat = True))
    fig.update_yaxes(
        range = [0, float(max(weight_values + target_values)) * 1.1],
    )
    context['plot'] = fig.to_html(
        full_html = False,
        include_plotlyjs = 'cdn',
    )
    
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