import os
import json
import google.generativeai as genai
from django.conf import settings
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView # Import APIView
from .models import JobPost, UserProfile
from .serializers import JobPostSerializer

class IsEmployer(permissions.BasePermission):
	def has_permission(self, request, view):
		if request.method in permissions.SAFE_METHODS:
			return True
		return (
			request.user.is_authenticated and
			hasattr(request.user, "profile") and
			request.user.profile.role == UserProfile.Role.EMPLOYER
		)

class JobPostViewSet(viewsets.ModelViewSet):
	queryset = JobPost.objects.all().order_by("-created_at")
	serializer_class = JobPostSerializer
	permission_classes = [IsEmployer]

	def perform_create(self, serializer):
		serializer.save(employer=self.request.user)

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def me(request):
	return Response({
		"uid": request.user.username,
		"email": request.user.email,
		"role": request.user.profile.role,
	})

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def set_role(request):
	role = request.data.get("role")
	if role not in (UserProfile.Role.EMPLOYER, UserProfile.Role.JOB_SEEKER):
		return Response({"error": "Invalid role"}, status=400)
	profile, _ = UserProfile.objects.get_or_create(user=request.user)
	profile.role = role
	profile.save()
	return Response({"role": role})

# --- ADD THE NEW AI-POWERED RECOMMENDATION VIEW ---

# Configure the Gemini API client
try:
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
except Exception as e:
    print(f"Error configuring Gemini API: {e}")

class AIRecommendationsView(APIView):
    """
    An API view that accepts a job seeker's preferences and returns
    a list of jobs filtered and ranked by the Gemini AI.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Get the current user's profile
        try:
            user_profile = request.user.profile
            if user_profile.role != UserProfile.Role.JOB_SEEKER:
                return Response(
                    {"error": "Only job seekers can receive recommendations."},
                    status=status.HTTP_403_FORBIDDEN
                )
        except UserProfile.DoesNotExist:
            return Response({"error": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)

        # Get user preferences from the frontend request
        preferences = request.data.get('preferences', {})
        user_skills = request.data.get('skills', [])

        # Fetch all active job posts from the database
        all_jobs = JobPost.objects.filter(status='active')
        if not all_jobs.exists():
            return Response([], status=status.HTTP_200_OK) # Return empty if no jobs exist

        # Serialize job data to be sent to the AI
        job_serializer = JobPostSerializer(all_jobs, many=True)
        jobs_data = job_serializer.data

        # Construct a detailed prompt for the Gemini API
        prompt = self.construct_prompt(user_profile, preferences, user_skills, jobs_data)

        # Call the Gemini API
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            
            # Clean the response text to ensure it's valid JSON
            cleaned_response_text = response.text.strip().replace('```json', '').replace('```', '').strip()
            
            # Parse the AI's response to get the recommended job IDs
            recommended_job_ids = json.loads(cleaned_response_text)

        except json.JSONDecodeError:
            return Response({"error": "Failed to parse AI response."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": f"An error occurred with the AI service: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Filter and return the matched jobs
        matched_jobs_dict = {job.id: job for job in all_jobs if job.id in recommended_job_ids}
        ordered_matched_jobs = [matched_jobs_dict[job_id] for job_id in recommended_job_ids if job_id in matched_jobs_dict]

        final_serializer = JobPostSerializer(ordered_matched_jobs, many=True)
        return Response(final_serializer.data, status=status.HTTP_200_OK)

    def construct_prompt(self, profile, preferences, skills, jobs_data):
        """Helper method to build the prompt for the AI."""
        return f"""
        You are an expert AI career advisor. Your task is to analyze a list of available jobs and recommend the best matches for a user based on their profile and explicit preferences.

        **User Profile:**
        - Role: {profile.get_role_display()}
        - Skills: {', '.join(skills) if skills else "Not specified"}
        - Other Profile Data: (You can add more fields from the UserProfile model here if needed)

        **User's Current Search Preferences:**
        - Keywords: {preferences.get('search', 'any')}
        - Location: {preferences.get('location', 'any')}
        - Job Type: {preferences.get('jobType', 'any')}
        - Salary Range: {preferences.get('salaryRange', 'any')}
        - Experience Level: {preferences.get('experienceLevel', 'any')}

        **Available Jobs (JSON format):**
        {json.dumps(jobs_data, indent=2)}

        **Your Task:**
        Analyze all the available jobs and return a JSON array containing only the integer IDs of the jobs that are the best fit for the user, ordered from the absolute best match to the least. Do not include any explanations or other text outside of the JSON array.

        Example Response: [10, 5, 23]
        """