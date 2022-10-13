from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import *

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

    def create(self, validated_data):
    	user = UserProfile.objects.create(
    						username=validated_data['username'],
    						email=validated_data['email'],
    						phone=validated_data['phone'],
    						first_name=validated_data['first_name'],
    						last_name=validated_data['last_name'],
    						)
    	user.set_password(validated_data['password'])
    	user.save()
    	return user


class ImageWareHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageWareHouse
        fields = '__all__'