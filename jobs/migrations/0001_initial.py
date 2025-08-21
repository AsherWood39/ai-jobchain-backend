from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


def create_initial(apps, schema_editor):
	# No data ops required
	pass


class Migration(migrations.Migration):

	initial = True

	dependencies = [
		('auth', '0012_alter_user_first_name_max_length'),
	]

	operations = [
		migrations.CreateModel(
			name='UserProfile',
			fields=[
				('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('role', models.CharField(choices=[('EMPLOYER', 'Employer'), ('JOB_SEEKER', 'Job Seeker')], default='JOB_SEEKER', max_length=16)),
				('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
			],
		),
		migrations.CreateModel(
			name='JobPost',
			fields=[
				('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('title', models.CharField(max_length=120)),
				('description', models.TextField()),
				('location', models.CharField(blank=True, max_length=120)),
				('company', models.CharField(blank=True, max_length=120)),
				('created_at', models.DateTimeField(auto_now_add=True)),
				('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_posts', to=settings.AUTH_USER_MODEL)),
			],
		),
		migrations.RunPython(create_initial, reverse_code=migrations.RunPython.noop),
	]
