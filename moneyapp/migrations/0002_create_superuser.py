from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_or_update_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    username = 'brian'  # Replace with your superuser username
    password = 'Brian2025'  # Replace with your desired password
    try:
        user = User.objects.get(username=username, is_superuser=True)
        user.password = make_password(password)
        user.save()
    except User.DoesNotExist:
        # Optionally create the superuser if it doesn’t exist
        User.objects.create_superuser(username, 'brian@example.com', password)

class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),  # Adjust if needed
        ('moneyapp', '0001_initial'),  # Your app’s previous migration
    ]

    operations = [
        migrations.RunPython(create_or_update_superuser),
    ]