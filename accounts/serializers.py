from dataclasses import fields
from rest_framework import serializers



# Model Import 
from django.contrib.auth.models import User
from .models import UserProfile




# Django User Serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields= "__all__"


# UserProfile List Data Serializers
class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        depth=1
        fields="__all__"



# UserProfile Serializers fror patch data
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    # album_musician= UserSerializer(many=True)
    
    class Meta:
        model = UserProfile
        fields ="__all__"
        depth =1