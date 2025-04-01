from django.db import migrations
from django.contrib.auth.hashers import make_password

def force_superuser_again(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    username = 'brian'
    password = 'Brian2025'
    email = 'brian@example.com'
    # Delete any existing user to avoid duplicates
    User.objects.filter(username=username).delete()
    # Create the superuser
    User.objects.create_superuser(username, email, password)

class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('moneyapp', '0001_initial'),  # Changed to 0001_initial
    ]

    operations = [
        migrations.RunPython(force_superuser_again),
    ]