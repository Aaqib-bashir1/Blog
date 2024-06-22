# yourapp/backends.py

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

CustomUser = get_user_model()
class EmailBackend(BaseBackend):
    def authenticate(self,request,  email=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
# # users/backends.py
# import logging
# from django.contrib.auth.backends import BaseBackend
# from django.contrib.auth import get_user_model
#
# CustomUser = get_user_model()
#
#
# class EmailBackend(BaseBackend):
#     def authenticate(self, request, email=None, password=None, **kwargs):
#         logger = logging.getLogger(__name__)
#         logger.debug(f"Attempting to authenticate user with email: {email}")
#
#         try:
#             user = CustomUser.objects.get(email=email)
#             if user.check_password(password):
#                 logger.debug("Authentication successful")
#                 return user
#             else:
#                 logger.debug("Authentication failed: Incorrect password")
#         except CustomUser.DoesNotExist:
#             logger.debug("Authentication failed: User does not exist")
#             return None
#
#     def get_user(self, user_id):
#         try:
#             return CustomUser.objects.get(pk=user_id)
#         except CustomUser.DoesNotExist:
#             return None
