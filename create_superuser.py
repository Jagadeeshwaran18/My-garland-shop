import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garland_shop.settings')
django.setup()

from django.contrib.auth.models import User

# Create superuser if it doesn't exist
username = 'admin'
email = 'admin@example.com'
password = 'admin123'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superuser created successfully!')
    print(f'Username: {username}')
    print(f'Password: {password}')
else:
    print(f'User "{username}" already exists!')
    print('To create a new superuser, run: python manage.py createsuperuser')

