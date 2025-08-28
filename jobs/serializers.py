from rest_framework import serializers
from .models import JobPost, Skill


class SkillSerializer(serializers.ModelSerializer):
	class Meta:
		model = Skill
		fields = ['id', 'name']


class JobPostSerializer(serializers.ModelSerializer):
	employer_name = serializers.CharField(source="employer.username", read_only=True)
	type = serializers.CharField(source="job_type", read_only=True)
	applications = serializers.IntegerField(source="applications_count", read_only=True)
	postedDate = serializers.DateTimeField(source="created_at", read_only=True)
	skills = SkillSerializer(many=True, read_only=True)
	skill_ids = serializers.PrimaryKeyRelatedField(source='skills', write_only=True, many=True, queryset=Skill.objects.all(), required=False)

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
			"skills",
			"skill_ids",
			"applications",
			"postedDate",
			"created_at",
			"employer_name",
		]
		
	def create(self, validated_data):
		skills_data = validated_data.pop('skills', [])
		job_post = JobPost.objects.create(**validated_data)
		if skills_data:
			job_post.skills.set(skills_data)
		return job_post
		
	def update(self, instance, validated_data):
		skills_data = validated_data.pop('skills', None)
		instance = super().update(instance, validated_data)
		if skills_data is not None:
			instance.skills.set(skills_data)
		return instance
