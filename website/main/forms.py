from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(
        required = True,
        label = 'Email',
    )
    password = forms.CharField(
        required = True,
        label = 'Password',
        widget = forms.PasswordInput,
    )