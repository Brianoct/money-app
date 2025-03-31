from django.db import migrations
from django.contrib.auth.hashers import make_password

def update_superuser_password(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    username = 'brian'
    new_password = 'Brian2025'
    email = 'brian@example.com'  # Optional, but recommended
    try:
        user = User.objects.get(username=username, is_superuser=True)
        user.password = make_password(new_password)
        user.save()
    except User.DoesNotExist:
        # Create the superuser if it doesn’t exist
        User.objects.create_superuser(username, email, new_password)

class Migration(migrations.Migration):
    dependencies = [
        ('moneyapp', '0001_initial'),  # Verify this matches your previous migration
    ]

    operations = [
        migrations.RunPython(update_superuser_password),
    ]