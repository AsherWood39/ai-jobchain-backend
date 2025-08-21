from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from jobs.views import JobPostViewSet, me, set_role

router = DefaultRouter()
router.register('jobs', JobPostViewSet, basename='job')

urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/', include(router.urls)),
	path('api/me', me),
	path('api/set-role', set_role),
]
