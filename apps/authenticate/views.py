from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
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

@login_required
def profile(request):
    """User profile view."""
    # Update the template path - the original was likely incorrect
    return render(request, 'cotton/authenticate/pages/profile.html', {'title': 'My Profile'})

@login_required
def profile_work(request):
    """User work history view."""
    return render(request, 'cotton/authenticate/pages/profile_work.html', {'title': 'Work History'})

@login_required
def profile_education(request):
    """User education history view."""
    return render(request, 'cotton/authenticate/pages/profile_education.html', {'title': 'Education History'})

@login_required
def profile_address(request):
    """User address view."""
    return render(request, 'cotton/authenticate/pages/profile_address.html', {'title': 'Address Information'})

@login_required
def change_password(request):
    """Change password view."""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('auth:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'cotton/authenticate/pages/change_password.html', {
        'form': form,
        'title': 'Change Password'
    })

@login_required
def edit_profile(request):
    """User profile edit view."""
    if request.method == 'POST':
        # Handle form submission (you'll need to create a form for this)
        # This is a placeholder implementation
        # Update user profile data based on form input
        messages.success(request, 'Profile updated successfully!')
        return redirect('auth:profile')
    
    # Display the edit form
    return render(request, 'cotton/authenticate/pages/edit_profile.html', {'title': 'Edit Profile'})
