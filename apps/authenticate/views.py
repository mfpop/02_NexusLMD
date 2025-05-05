import logging
import time
import io
from PIL import Image
import base64

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Set up logging
logger = logging.getLogger(__name__)


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
    return render(request, 'cotton/authenticate/pages/register.html', {'form': form, 'title': 'Register'})

@login_required
def profile(request):
    """User profile view."""
    # Update the template path - the original was likely incorrect
    return render(request, 'cotton/authenticate/pages/profile.html', {'title': 'My Profile'})

@login_required
def profile_work(request):
    """User work history view."""
    from .models import WorkExperience
    from django.http import JsonResponse
    import json
    from datetime import datetime
    
    if request.method == 'POST':
        # Handle adding new work experience
        try:
            company = request.POST.get('company')
            position = request.POST.get('position')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            description = request.POST.get('description')
            
            # Validate required fields
            if not company or not position or not start_date:
                messages.error(request, 'Company, position, and start date are required fields')
                return redirect('auth:profile_work')
            
            # Create new work experience
            work_exp = WorkExperience(
                user=request.user,
                company=company,
                position=position,
                start_date=start_date,
                description=description
            )
            
            # End date is optional
            if end_date:
                work_exp.end_date = end_date
                
            work_exp.save()
            messages.success(request, 'Work experience added successfully!')
            
        except Exception as e:
            messages.error(request, f'Error adding work experience: {str(e)}')
        
        return redirect('auth:profile_work')
    
    # Get all work experiences for the user
    work_experiences = WorkExperience.objects.filter(user=request.user)
    
    # Serialize work experiences
    serialized_experiences = []
    for exp in work_experiences:
        serialized_experiences.append({
            'id': exp.id,
            'company': exp.company,
            'position': exp.position,
            'start_date': exp.start_date.strftime('%Y-%m-%d'),
            'end_date': exp.end_date.strftime('%Y-%m-%d') if exp.end_date else None,
            'description': exp.description or ''
        })
    
    return render(
        request, 
        'cotton/authenticate/pages/profile_work.html', 
        {
            'title': 'Work History',
            'work_experiences': json.dumps(serialized_experiences)
        }
    )

@login_required
def profile_education(request):
    """User education history view."""
    from .models import EducationExperience
    from django.http import JsonResponse
    import json
    from datetime import datetime
    
    # Get all education experiences for the user
    education_experiences = EducationExperience.objects.filter(user=request.user)
    
    return render(
        request, 
        'cotton/authenticate/pages/profile_education.html', 
        {
            'title': 'Education History',
            'education_experiences': education_experiences
        }
    )

@login_required
def profile_address(request):
    """User address view with save functionality."""
    from apps.authenticate.models import Profile
    
    if request.method == 'POST':
        user = request.user
        try:
            profile = user.profile
        except Profile.DoesNotExist:
            profile = Profile(user=user)
        
        # Update address fields
        profile.address = request.POST.get('address', '')
        profile.city = request.POST.get('city', '')
        profile.state = request.POST.get('state', '')
        profile.postal_code = request.POST.get('postal_code', '')
        profile.country = request.POST.get('country', '')
        
        try:
            profile.save()
            messages.success(request, 'Address updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating address: {str(e)}')
        
        return redirect('auth:profile_address')
    
    # List of countries for the dropdown
    countries = [
        'United States', 'Canada', 'Mexico', 'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola',
        'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas',
        'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia',
        'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi',
        'Cabo Verde', 'Cambodia', 'Cameroon', 'Central African Republic', 'Chad', 'Chile', 'China',
        'Colombia', 'Comoros', 'Congo', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic',
        'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador',
        'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Fiji', 'Finland', 'France',
        'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea',
        'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia',
        'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan',
        'Kenya', 'Kiribati', 'Korea, North', 'Korea, South', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos',
        'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg',
        'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania',
        'Mauritius', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique',
        'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger',
        'Nigeria', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Panama', 'Papua New Guinea',
        'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia', 'Rwanda',
        'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino',
        'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone',
        'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Sudan',
        'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan',
        'Tanzania', 'Thailand', 'Timor-Leste', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey',
        'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'Uruguay',
        'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe'
    ]
    
    return render(request, 'cotton/authenticate/pages/profile_address.html', {
        'title': 'Address Information',
        'countries': sorted(countries)
    })

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
    from apps.authenticate.models import Profile
    import json
    from django.http import JsonResponse
    
    if request.method == 'POST':
        try:
            # Get the user and profile
            user = request.user
            try:
                profile = user.profile
            except Profile.DoesNotExist:
                # Create profile if it doesn't exist
                profile = Profile(user=user)
            
            # Update user fields
            if 'first_name' in request.POST:
                user.first_name = request.POST.get('first_name')
            
            if 'last_name' in request.POST:
                user.last_name = request.POST.get('last_name')
            
            # Save user changes
            user.save()
            
            # Update profile fields
            profile_fields = [
                'phone', 'title', 'bio', 
                'address', 'city', 'state', 'postal_code', 'country'
            ]
            
            for field in profile_fields:
                if field in request.POST:
                    setattr(profile, field, request.POST.get(field))
            
            # Save profile changes
            profile.save()
            
            # If this is an HTMX request, return success response
            if request.headers.get('HX-Request'):
                return HttpResponse(status=200)
                
            messages.success(request, 'Profile updated successfully!')
            return redirect('auth:profile')
        
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            logger.error(f"Profile update error: {str(e)}")
            logger.error(error_trace)
            
            # If this is an HTMX request, return error response
            if request.headers.get('HX-Request'):
                return HttpResponse(f"Error updating profile: {str(e)}", status=500)
                
            messages.error(request, f'Error updating profile: {str(e)}')
            return redirect('auth:profile')
    
    # If not POST, redirect to the profile page
    return redirect('auth:profile')

@login_required
@csrf_exempt
def update_avatar(request):
    """Avatar update function with validation."""
    try:
        if request.method == 'POST' and request.FILES.get('avatar'):
            # Get the file
            image_file = request.FILES['avatar']
            
            print(f"Avatar upload attempt by {request.user.username}: {image_file.name}, {image_file.size} bytes")
            
            # Validate file type
            valid_types = ['image/jpeg', 'image/png', 'image/gif']
            if image_file.content_type not in valid_types:
                print(f"Invalid file type: {image_file.content_type}")
                return HttpResponse(
                    "Invalid file type. Please select a JPEG, PNG, or GIF image.",
                    status=400
                )
            
            # Validate file size (2MB limit)
            if image_file.size > 2 * 1024 * 1024:
                print(f"File too large: {image_file.size} bytes")
                return HttpResponse(
                    "File size exceeds 2MB limit. Please select a smaller image.",
                    status=400
                )
            
            # Read file data
            file_data = image_file.read()
            print(f"Successfully read file data: {len(file_data)} bytes")
            
            # Encode to base64
            encoded = base64.b64encode(file_data).decode('utf-8')
            print(f"Successfully encoded to base64: {len(encoded)} characters")
            
            # Get or create profile for the user
            from apps.authenticate.models import Profile
            try:
                profile = request.user.profile
                print(f"Found existing profile for user: {request.user.username}")
            except Profile.DoesNotExist:
                # Create a profile if it doesn't exist
                profile = Profile(user=request.user)
                profile.save()
                print(f"Created new profile for user: {request.user.username}")
            
            # Save avatar data to profile
            print(f"Previous avatar data length: {len(profile.avatar_data or '')}")
            profile.avatar_data = encoded
            print(f"New avatar data length: {len(profile.avatar_data or '')}")
            profile.save()
            print(f"Profile saved successfully")
            
            # Force a database commit
            from django.db import transaction
            transaction.commit()
            print(f"Transaction committed")
            
            # Verify the save worked
            profile.refresh_from_db()
            print(f"Verified avatar data in database: {len(profile.avatar_data or '')} characters")
            
            # Redirect to the profile page to see the updated avatar
            messages.success(request, "Avatar updated successfully!")
            return redirect('auth:profile')
            
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Avatar upload error: {str(e)}")
        print(error_trace)
        messages.error(request, f"Error uploading avatar: {str(e)}")
        return redirect('auth:profile')
    
    return redirect('auth:profile')

@login_required
def update_work_experience(request):
    """Update existing work experience."""
    from .models import WorkExperience
    from django.http import JsonResponse
    import json
    import logging
    
    logger = logging.getLogger(__name__)
    
    if request.method == 'POST':
        try:
            logger.info("Processing update_work_experience request")
            data = json.loads(request.body)
            exp_id = data.get('id')
            
            logger.info(f"Updating work experience ID: {exp_id}")
            
            work_exp = WorkExperience.objects.get(id=exp_id, user=request.user)
            
            # Update fields
            work_exp.company = data.get('company', work_exp.company)
            work_exp.position = data.get('position', work_exp.position)
            
            if data.get('startDate'):
                work_exp.start_date = data.get('startDate')
            if data.get('endDate'):
                work_exp.end_date = data.get('endDate')
            if data.get('description') is not None:
                work_exp.description = data.get('description')
                
            work_exp.save()
            logger.info(f"Work experience updated: {work_exp.id}")
            
            if request.headers.get('HX-Request'):
                # Get updated work experiences
                work_experiences = WorkExperience.objects.filter(user=request.user)
                # Return the updated work experience template
                return render(
                    request,
                    'cotton/authenticate/pages/profile_work.html',
                    {
                        'work_experiences': work_experiences
                    }
                )
                
            messages.success(request, 'Work experience updated successfully!')
            
        except WorkExperience.DoesNotExist:
            logger.warning(f"Work experience not found: ID {data.get('id') if 'data' in locals() else 'unknown'}")
            if request.headers.get('HX-Request'):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Work experience not found.'
                }, status=404)
            messages.error(request, 'Work experience not found.')
            
        except Exception as e:
            logger.error(f"Error updating work experience: {str(e)}")
            if request.headers.get('HX-Request'):
                return JsonResponse({
                    'status': 'error',
                    'message': f'Error updating work experience: {str(e)}'
                }, status=500)
            messages.error(request, f'Error updating work experience: {str(e)}')
    
    return redirect('auth:profile_work')

@login_required
def delete_work_experience(request):
    """Delete a work experience."""
    from .models import WorkExperience
    from django.http import JsonResponse
    import json
    
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            exp_id = data.get('id')
            work_exp = WorkExperience.objects.get(id=exp_id, user=request.user)
            work_exp.delete()
            
            return JsonResponse({'status': 'success'})
        
        except WorkExperience.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Work experience not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

@login_required
def add_work_experience(request):
    """Add a new work experience."""
    from .models import WorkExperience
    import json
    from django.http import JsonResponse
    import logging
    
    logger = logging.getLogger(__name__)
    
    if request.method == 'POST':
        try:
            logger.info("Processing add_work_experience request")
            # Check if this is an HTMX request with JSON data
            if request.headers.get('HX-Request') and 'application/json' in request.headers.get('Content-Type', ''):
                data = json.loads(request.body)
                logger.info(f"Received JSON data: {data}")
                
                # Extract data from the request
                company = data.get('company')
                position = data.get('position')
                start_date = data.get('startDate')
                end_date = data.get('endDate')
                description = data.get('description')
            else:
                # Regular form submission
                company = request.POST.get('company')
                position = request.POST.get('position')
                start_date = request.POST.get('start_date')
                end_date = request.POST.get('end_date')
                description = request.POST.get('description')
                logger.info(f"Received form data - company: {company}, position: {position}")
            
            # Validate required fields
            if not company or not position or not start_date:
                if request.headers.get('HX-Request'):
                    logger.warning("Missing required fields in HTMX request")
                    return JsonResponse({
                        'status': 'error', 
                        'message': 'Company, position, and start date are required fields'
                    }, status=400)
                messages.error(request, 'Company, position, and start date are required fields')
                return redirect('auth:profile_work')
            
            # Create new work experience
            work_exp = WorkExperience(
                user=request.user,
                company=company,
                position=position,
                start_date=start_date,
                description=description
            )
            
            # End date is optional
            if end_date:
                work_exp.end_date = end_date
                
            work_exp.save()
            logger.info(f"Work experience saved with ID: {work_exp.id}")
            
            if request.headers.get('HX-Request'):
                # Get updated work experiences
                work_experiences = WorkExperience.objects.filter(user=request.user)
                # Return the updated work experience template
                return render(
                    request,
                    'cotton/authenticate/pages/profile_work.html',
                    {
                        'work_experiences': work_experiences
                    }
                )
                
            messages.success(request, 'Work experience added successfully!')
            
        except Exception as e:
            logger.error(f"Error in add_work_experience: {str(e)}")
            if request.headers.get('HX-Request'):
                return JsonResponse({
                    'status': 'error', 
                    'message': f'Error adding work experience: {str(e)}'
                }, status=500)
            messages.error(request, f'Error adding work experience: {str(e)}')
        
    return redirect('auth:profile_work')

@login_required
def update_education_experience(request):
    """Update existing education experience."""
    from .models import EducationExperience
    from django.http import JsonResponse
    import json
    import logging
    
    logger = logging.getLogger(__name__)
    
    if request.method == 'POST':
        try:
            logger.info("Processing update_education_experience request")
            data = json.loads(request.body)
            exp_id = data.get('id')
            
            logger.info(f"Updating education experience ID: {exp_id}")
            
            edu_exp = EducationExperience.objects.get(id=exp_id, user=request.user)
            
            # Update fields
            edu_exp.institution = data.get('institution', edu_exp.institution)
            edu_exp.degree = data.get('degree', edu_exp.degree)
            edu_exp.field_of_study = data.get('fieldOfStudy', edu_exp.field_of_study)
            
            if data.get('startDate'):
                edu_exp.start_date = data.get('startDate')
            if data.get('endDate'):
                edu_exp.end_date = data.get('endDate')
            if data.get('description') is not None:
                edu_exp.description = data.get('description')
                
            edu_exp.save()
            logger.info(f"Education experience updated: {edu_exp.id}")
            
            if request.headers.get('HX-Request'):
                # Get updated education experiences
                education_experiences = EducationExperience.objects.filter(user=request.user)
                # Return the updated education experience template
                return render(
                    request,
                    'cotton/authenticate/pages/profile_education.html',
                    {
                        'education_experiences': education_experiences
                    }
                )
                
            messages.success(request, 'Education experience updated successfully!')
            
        except EducationExperience.DoesNotExist:
            logger.warning(f"Education experience not found: ID {data.get('id') if 'data' in locals() else 'unknown'}")
            if request.headers.get('HX-Request'):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Education experience not found.'
                }, status=404)
            messages.error(request, 'Education experience not found.')
            
        except Exception as e:
            logger.error(f"Error updating education experience: {str(e)}")
            if request.headers.get('HX-Request'):
                return JsonResponse({
                    'status': 'error',
                    'message': f'Error updating education experience: {str(e)}'
                }, status=500)
            messages.error(request, f'Error updating education experience: {str(e)}')
    
    return redirect('auth:profile_education')

@login_required
def delete_education_experience(request):
    """Delete an education experience."""
    from .models import EducationExperience
    from django.http import JsonResponse
    import json
    
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            exp_id = data.get('id')
            edu_exp = EducationExperience.objects.get(id=exp_id, user=request.user)
            edu_exp.delete()
            
            if request.headers.get('HX-Request'):
                # Get updated education experiences
                education_experiences = EducationExperience.objects.filter(user=request.user)
                # Return the updated education experience template
                return render(
                    request,
                    'cotton/authenticate/pages/profile_education.html',
                    {
                        'education_experiences': education_experiences
                    }
                )
            
            return JsonResponse({'status': 'success'})
        
        except EducationExperience.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Education experience not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

@login_required
def add_education_experience(request):
    """Add a new education experience."""
    from .models import EducationExperience
    import json
    from django.http import JsonResponse
    import logging
    
    logger = logging.getLogger(__name__)
    
    if request.method == 'POST':
        try:
            logger.info("Processing add_education_experience request")
            # Check if this is an HTMX request with JSON data
            if request.headers.get('HX-Request') and 'application/json' in request.headers.get('Content-Type', ''):
                data = json.loads(request.body)
                logger.info(f"Received JSON data: {data}")
                
                # Extract data from the request
                institution = data.get('institution')
                degree = data.get('degree')
                field_of_study = data.get('fieldOfStudy')
                start_date = data.get('startDate')
                end_date = data.get('endDate')
                description = data.get('description')
            else:
                # Regular form submission
                institution = request.POST.get('institution')
                degree = request.POST.get('degree')
                field_of_study = request.POST.get('field_of_study')
                start_date = request.POST.get('start_date')
                end_date = request.POST.get('end_date')
                description = request.POST.get('description')
                logger.info(f"Received form data - institution: {institution}, degree: {degree}")
            
            # Validate required fields
            if not institution or not degree or not start_date:
                if request.headers.get('HX-Request'):
                    logger.warning("Missing required fields in HTMX request")
                    return JsonResponse({
                        'status': 'error', 
                        'message': 'Institution, degree, and start date are required fields'
                    }, status=400)
                messages.error(request, 'Institution, degree, and start date are required fields')
                return redirect('auth:profile_education')
            
            # Create new education experience
            edu_exp = EducationExperience(
                user=request.user,
                institution=institution,
                degree=degree,
                field_of_study=field_of_study,
                start_date=start_date,
                description=description
            )
            
            # End date is optional
            if end_date:
                edu_exp.end_date = end_date
                
            edu_exp.save()
            logger.info(f"Education experience saved with ID: {edu_exp.id}")
            
            if request.headers.get('HX-Request'):
                # Get updated education experiences
                education_experiences = EducationExperience.objects.filter(user=request.user)
                # Return the updated education experience template
                return render(
                    request,
                    'cotton/authenticate/pages/profile_education.html',
                    {
                        'education_experiences': education_experiences
                    }
                )
                
            messages.success(request, 'Education experience added successfully!')
            
        except Exception as e:
            logger.error(f"Error in add_education_experience: {str(e)}")
            if request.headers.get('HX-Request'):
                return JsonResponse({
                    'status': 'error', 
                    'message': f'Error adding education experience: {str(e)}'
                }, status=500)
            messages.error(request, f'Error adding education experience: {str(e)}')
        
    return redirect('auth:profile_education')
