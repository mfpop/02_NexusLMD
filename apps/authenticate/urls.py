from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = 'auth'

urlpatterns = [
    path('', views.index, name='auth_home'),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='cotton/authenticate/pages/login.html'),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='auth:login', http_method_names=['get', 'post']),
        name='logout'
    ),
    path('register/', views.register, name='register'),
    # Adding profile-related paths
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),  # Add this line
    path('profile/work/', views.profile_work, name='profile_work'),
    path('profile/education/', views.profile_education, name='profile_education'),
    path('profile/address/', views.profile_address, name='profile_address'),
    path('password/', views.change_password, name='change_password'),
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='cotton/authenticate/pages/password_reset.html'
        ),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='cotton/authenticate/pages/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='cotton/authenticate/pages/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='cotton/authenticate/pages/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
    # Fix Change Password URL Path
    path('profile/change-password/', RedirectView.as_view(pattern_name='auth:change_password'), name='profile_change_password'),
]
