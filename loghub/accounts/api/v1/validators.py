from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from accounts import models

def validate_new_password(new_password, request):
 
    try:
        validate_password(new_password, request)
    except ValidationError as e:
        raise serializers.ValidationError(e.messages)


def validate_profile(new_password,password, request):
    user = request.user

    if new_password:
        if not password:
            raise serializers.ValidationError({"password": "Current password is required."})
        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Current password is incorrect."})

        validate_new_password(new_password,request)







def validate_level(self, value):
        if value not in dict(models.Professional.LEVEL_CHOICES).keys():
            raise serializers.ValidationError("Invalid level choice.")
        
        return value