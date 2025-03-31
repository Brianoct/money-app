from django.db import migrations
from django.contrib.auth.hashers import make_password

def update_superuser_password(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    username = 'brian'  # Replace with your actual superuser username
    new_password = 'Brian2025'  # Replace with your desired password
    try:
        user = User.objects.get(username=username, is_superuser=True)
        user.password = make_password(new_password)
        user.save()
    except User.DoesNotExist:
        pass  # Optionally, create the user if it doesn't exist

class Migration(migrations.Migration):
    dependencies = [
        ('moneyapp', '0001_initial'),  # Adjust to your previous migration
    ]

    operations = [
        migrations.RunPython(update_superuser_password),
    ]