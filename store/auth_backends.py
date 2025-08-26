from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from .models import UserProfile

class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try email
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            # Try phone
            try:
                profile = UserProfile.objects.get(phone=username)
                user = profile.user
            except UserProfile.DoesNotExist:
                return None
        if user.check_password(password):
            return user
        return None