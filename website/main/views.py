from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from .forms import LoginForm

def index_view(request):
    return render(request, 'main/index.html')
    
def about_view(request):
    return render(request, 'main/about.html')
    
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                email = form.cleaned_data['email'],
                password = form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('main:index')
            else:
                error_message = 'Invalid username or password.'
                context = {
                    'login_form': form,
                    'error_message': error_message,
                }
                return render(request, 'main/login.html', context = context)
        else:
            error_message = 'Invalid values in form fields.'
            context = {
                'login_form': form,
                'error_message': error_message,
            }
            return render(request, 'main/login.html', context = context)
    else:
        form = LoginForm()
    return render(request, 'main/login.html', context = {'login_form': form})