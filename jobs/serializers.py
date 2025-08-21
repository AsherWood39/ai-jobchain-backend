from rest_framework import serializers
from .models import JobPost


class JobPostSerializer(serializers.ModelSerializer):
	employer_name = serializers.CharField(source="employer.username", read_only=True)
	type = serializers.CharField(source="job_type", read_only=True)
	applications = serializers.IntegerField(source="applications_count", read_only=True)
	postedDate = serializers.DateTimeField(source="created_at", read_only=True)

	class Meta:
		model = JobPost
		fields = [
			"id",
			"title",
			"description",
			"location",
			"company",
			"salary",
			"type",
			"status",
			"applications",
			"postedDate",
			"created_at",
			"employer_name",
		]
