# backends.py
import hashlib
from django.contrib.auth.backends import ModelBackend
from .models import CustomUser
from django.contrib.auth.hashers import check_password

class CustomUserBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=email)
            
            if check_password(password,user.password):
                return user
        except CustomUser.DoesNotExist:
            return None

        return None
