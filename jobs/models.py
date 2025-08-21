from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
	class Role(models.TextChoices):
		EMPLOYER = "EMPLOYER", "Employer"
		JOB_SEEKER = "JOB_SEEKER", "Job Seeker"

	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
	role = models.CharField(max_length=16, choices=Role.choices, default=Role.JOB_SEEKER)

	def __str__(self) -> str:
		return f"{self.user.username} ({self.role})"


class JobPost(models.Model):
	class JobType(models.TextChoices):
		FULL_TIME = "FULL_TIME", "Full Time"
		PART_TIME = "PART_TIME", "Part Time"
		CONTRACT = "CONTRACT", "Contract"
		INTERNSHIP = "INTERNSHIP", "Internship"
		FREELANCE = "FREELANCE", "Freelance"

	class JobStatus(models.TextChoices):
		ACTIVE = "active", "Active"
		CLOSED = "closed", "Closed"
		DRAFT = "draft", "Draft"

	employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="job_posts")
	title = models.CharField(max_length=120)
	description = models.TextField()
	location = models.CharField(max_length=120, blank=True)
	company = models.CharField(max_length=120, blank=True)
	salary = models.CharField(max_length=100, blank=True)
	job_type = models.CharField(max_length=20, choices=JobType.choices, default=JobType.FULL_TIME)
	status = models.CharField(max_length=10, choices=JobStatus.choices, default=JobStatus.ACTIVE)
	applications_count = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return self.title
