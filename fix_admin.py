import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garland_shop.settings')
django.setup()

from django.contrib.auth.models import User

# Find or create admin user and ensure they are staff
admin_user = User.objects.filter(username='admin').first()

if admin_user:
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.save()
    print(f'Admin user "{admin_user.username}" has been set as staff and superuser.')
    print(f'Is staff: {admin_user.is_staff}')
    print(f'Is superuser: {admin_user.is_superuser}')
else:
    print('Admin user not found. Please create it using: python manage.py createsuperuser')
    print('Make sure to use username "admin" when creating.')

