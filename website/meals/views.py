from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ComponentDefinitionForm
from .models import ComponentGroup

@login_required
def index_view(request):
    return render(request, 'meals/index.html')
    
@login_required
def component_definitions_view(request):

    #Prepare a context dictionary:
    context = {
        'definition_form': ComponentDefinitionForm(),
    }

    #If this is a post request, determine the submitted form and handle it:
    if request.method == 'POST':
        match request.POST.get('form_name'):
            case 'add_definition':
                form = ComponentDefinitionForm(request.POST)
                if form.is_valid():
                    obj = form.save(commit = False)
                    obj.user_id = request.user.id
                    obj.save()
                else:
                    context['definition_form'] = form
    
    #Render the page:
    return render(request, 'meals/component_definitions.html', context)


@login_required
def component_groups_view(request):

    #Prepare a context dictionary:
    context = {
        'component_groups': ComponentGroup.objects.filter(
            user_id = request.user.id,
        ).order_by(
            'name'
        ),
    }

    #If this is a post request, determine the submitted form and handle it:
    if request.method == 'POST':
        match request.POST.get('form_name'):
            case 'delete_group':
                try:
                    id = int(request.POST.get('group_id'))
                    context['component_groups'].get(pk = id).delete()
                except:
                    pass #Suggests malicious
        return redirect('meals:component_groups')
                    
    
    #Render the page:
    return render(request, 'meals/component_groups.html', context)
