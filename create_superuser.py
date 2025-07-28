#!/usr/bin/env python
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create superuser if it doesn't exist
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    print("Superuser created successfully!")
    print("Username: admin")
    print("Password: admin123")
else:
    print("Superuser 'admin' already exists!") 