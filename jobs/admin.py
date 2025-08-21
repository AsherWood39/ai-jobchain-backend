from django.contrib import admin
from .models import UserProfile, JobPost


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ("user", "role")
	search_fields = ("user__username", "user__email", "role")


@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
	list_display = ("title", "company", "employer", "created_at")
	search_fields = ("title", "company", "employer__username")
	list_filter = ("created_at",)
