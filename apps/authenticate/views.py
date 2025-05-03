from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


def index(request):
    """Index view for the authentication app."""
    return render(request, 'index.html', {'title': 'Authentication'})

def register(request):
    """User registration view."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, 
                f'Account created for {username}. You can now log in.'
            )
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'authenticate/register.html', {'form': form, 'title': 'Register'})
