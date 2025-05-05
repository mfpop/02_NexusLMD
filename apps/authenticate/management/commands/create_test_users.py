import random
import base64
from datetime import datetime, timedelta
from io import BytesIO
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from apps.authenticate.models import Profile, WorkExperience, EducationExperience
from faker import Faker
import requests
from PIL import Image

fake = Faker()

def get_random_avatar():
    """Get a random avatar from a placeholder service and convert to base64"""
    try:
        # Get a random avatar from randomuser.me API
        response = requests.get('https://randomuser.me/api/portraits/men/{}.jpg'.format(random.randint(1, 99)))
        if response.status_code == 200:
            # Convert the image to base64
            img = Image.open(BytesIO(response.content))
            # Resize image to a reasonable size
            img = img.resize((200, 200))
            buffer = BytesIO()
            img.save(buffer, format="JPEG")
            img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
            return img_str
    except Exception as e:
        print(f"Error getting random avatar: {e}")
    
    return None

class Command(BaseCommand):
    help = 'Create 10 test users with complete profile information'
    
    def handle(self, *args, **options):
        self.stdout.write('Creating 10 test users with complete profiles...')
        
        # List of company names for generating work experience
        companies = [
            "Tech Innovations Inc.", "Global Solutions Ltd.", "Future Systems", 
            "Data Dynamics", "Smart Networks", "Cloud Computing Solutions",
            "Digital Transformation Group", "Infinite Software", "NextGen Technologies",
            "AI Solutions Hub", "Cyber Security Partners", "Quantum Computing Labs"
        ]
        
        # List of positions for generating work experience
        positions = [
            "Software Developer", "Project Manager", "System Analyst",
            "Data Scientist", "Product Manager", "UX Designer",
            "DevOps Engineer", "Network Administrator", "Security Specialist",
            "Business Analyst", "Full Stack Developer", "Quality Assurance Engineer"
        ]
        
        # List of institutions for generating education experience
        institutions = [
            "MIT", "Stanford University", "Harvard University", "Oxford University",
            "Cambridge University", "California Institute of Technology", "Yale University",
            "Princeton University", "University of Chicago", "Columbia University",
            "University of Pennsylvania", "Cornell University"
        ]
        
        # List of degrees for generating education experience
        degrees = [
            "Bachelor of Science in Computer Science", "Master of Business Administration",
            "Bachelor of Arts in Economics", "Master of Science in Data Science",
            "PhD in Computer Engineering", "Bachelor of Science in Information Technology",
            "Master of Arts in Design", "Bachelor of Engineering", "Associate Degree in Web Development",
            "Bachelor of Science in Mathematics", "Master of Science in Cybersecurity"
        ]
        
        # List of fields of study
        fields = [
            "Computer Science", "Business Administration", "Economics", "Data Science",
            "Computer Engineering", "Information Technology", "Design", "Engineering",
            "Web Development", "Mathematics", "Cybersecurity", "Artificial Intelligence"
        ]
        
        # Create 10 test users
        for i in range(10):
            # Generate unique username
            username = f"{fake.user_name()}_{get_random_string(5)}"
            
            # Create user
            user = User.objects.create_user(
                username=username,
                email=fake.email(),
                password="testuser123",  # Simple password for testing
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )
            
            # Create or update profile
            try:
                profile = user.profile
            except Profile.DoesNotExist:
                profile = Profile(user=user)
            
            # Update profile fields
            profile.phone = fake.phone_number()
            profile.title = fake.job()
            profile.bio = fake.text(max_nb_chars=500)
            profile.address = fake.street_address()
            profile.city = fake.city()
            profile.state = fake.state()
            profile.postal_code = fake.postcode()
            profile.country = fake.country()
            profile.avatar_data = get_random_avatar()
            profile.save()
            
            # Generate 1-3 random work experiences
            num_work_experiences = random.randint(1, 3)
            for j in range(num_work_experiences):
                # Generate random dates (ensure they make sense chronologically)
                end_date_choice = random.choice([None, datetime.now().date() - timedelta(days=random.randint(30, 365))])
                start_date = datetime.now().date() - timedelta(days=random.randint(365, 1825))  # 1-5 years ago
                
                WorkExperience.objects.create(
                    user=user,
                    company=random.choice(companies),
                    position=random.choice(positions),
                    start_date=start_date,
                    end_date=end_date_choice,
                    description=fake.text(max_nb_chars=300)
                )
            
            # Generate 1-2 random education experiences
            num_education_experiences = random.randint(1, 2)
            for j in range(num_education_experiences):
                # Generate random dates (ensure they make sense chronologically)
                end_date_choice = random.choice([None, datetime.now().date() - timedelta(days=random.randint(30, 730))])
                start_date = datetime.now().date() - timedelta(days=random.randint(1460, 2920))  # 4-8 years ago
                
                EducationExperience.objects.create(
                    user=user,
                    institution=random.choice(institutions),
                    degree=random.choice(degrees),
                    field_of_study=random.choice(fields),
                    start_date=start_date,
                    end_date=end_date_choice,
                    description=fake.text(max_nb_chars=200)
                )
            
            self.stdout.write(self.style.SUCCESS(f'Created test user: {username}'))
        
        self.stdout.write(self.style.SUCCESS('Successfully created 10 test users with complete profiles!'))