# authentication_backends.py
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

class ContactNumberBackend(BaseBackend):
    def authenticate(self, request, contact_no=None, password=None):
        User = get_user_model()
        print("comes here inside")
        print(contact_no)
        print(password)
        try:
            user = User.objects.get(contact_no=contact_no)
        except User.DoesNotExist:
            return None
        
        print("comes here 1")
        print(user)

        if user.check_password(password):
            return user
        
        print("comes here 2")
        return None