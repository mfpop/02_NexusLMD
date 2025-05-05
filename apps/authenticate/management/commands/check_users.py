from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.authenticate.models import WorkExperience, EducationExperience

class Command(BaseCommand):
    help = 'Check how many users are in the database with their profile information'
    
    def handle(self, *args, **options):
        # Count users
        user_count = User.objects.count()
        self.stdout.write(f'Total users in database: {user_count}')
        
        # Show details of up to 5 users
        users = User.objects.all()[:5]
        for user in users:
            self.stdout.write(f'\nUsername: {user.username}')
            self.stdout.write(f'Name: {user.first_name} {user.last_name}')
            self.stdout.write(f'Email: {user.email}')
            
            # Check profile
            try:
                profile = user.profile
                self.stdout.write('Profile: YES')
                self.stdout.write(f'  - Bio: {"YES" if profile.bio else "NO"}')
                self.stdout.write(f'  - Avatar: {"YES" if profile.avatar_data else "NO"}')
                self.stdout.write(f'  - Address: {"YES" if profile.address else "NO"}')
            except Exception:
                self.stdout.write('Profile: NO')
            
            # Check work experience
            work_count = WorkExperience.objects.filter(user=user).count()
            self.stdout.write(f'Work experiences: {work_count}')
            
            # Check education experience
            edu_count = EducationExperience.objects.filter(user=user).count()
            self.stdout.write(f'Education experiences: {edu_count}')
            
            self.stdout.write('-' * 40)
            
        # Print message to guide next steps
        if user_count < 10:
            self.stdout.write(self.style.WARNING(f'\nOnly {user_count} users in database. Run "python manage.py create_test_users" to add 10 test users.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'\nYou have {user_count} users in the database.'))