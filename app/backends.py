from django.contrib.auth.backends import ModelBackend
from .models import User
from django.contrib.auth import get_user_model

class RoleBasedAuthBackend(ModelBackend):
    def authenticate(self, request, Username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Username=Username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None
    
    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None