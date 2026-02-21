import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garland_shop.settings')
django.setup()

from django.contrib.auth.models import User

# Create a regular user for testing
username = 'user'
email = 'user@example.com'
password = 'user123'

if not User.objects.filter(username=username).exists():
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    user.is_staff = False
    user.is_superuser = False
    user.save()
    print(f'Regular user created successfully!')
    print(f'Username: {username}')
    print(f'Password: {password}')
    print(f'Is Staff: {user.is_staff}')
else:
    existing_user = User.objects.get(username=username)
    existing_user.set_password(password)
    existing_user.is_staff = False
    existing_user.save()
    print(f'User "{username}" password updated!')
    print(f'Username: {username}')
    print(f'Password: {password}')
    print(f'Is Staff: {existing_user.is_staff}')

