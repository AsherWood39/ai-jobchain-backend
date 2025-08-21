from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import authentication, exceptions
import firebase_admin
from firebase_admin import auth as fb_auth, credentials
from .models import UserProfile
import os


def ensure_firebase_initialized():
	if firebase_admin._apps:
		return
	cert_path = getattr(settings, 'FIREBASE_CERT_PATH', None)
	if not cert_path or not os.path.isfile(cert_path):
		raise exceptions.AuthenticationFailed('Server auth not configured')
	cred = credentials.Certificate(cert_path)
	firebase_admin.initialize_app(cred)


class FirebaseAuthentication(authentication.BaseAuthentication):
	def authenticate(self, request):
		auth_header = request.META.get("HTTP_AUTHORIZATION", "")
		if not auth_header.startswith("Bearer "):
			return None

		id_token = auth_header.split(" ", 1)[1]
		try:
			ensure_firebase_initialized()
			decoded = fb_auth.verify_id_token(id_token)
		except exceptions.AuthenticationFailed:
			raise
		except Exception:
			raise exceptions.AuthenticationFailed("Invalid Firebase ID token")

		uid = decoded.get("uid")
		email = decoded.get("email", "")
		if not uid:
			raise exceptions.AuthenticationFailed("Invalid token payload")

		user, _ = User.objects.get_or_create(username=uid, defaults={"email": email})
		UserProfile.objects.get_or_create(user=user)
		return (user, None)
