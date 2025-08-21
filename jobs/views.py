from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
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
