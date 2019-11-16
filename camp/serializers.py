# backend/models/serializers.py
from rest_framework import serializers
from .models import User, Collective, MembersOfCollective
from django.conf import settings



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =  User
        fields = '__all__'

class UserFullSerializer(serializers.ModelSerializer):
    class Meta:
        model =  settings.AUTH_USER_MODEL
        fields = ("id", "last_login", "is_superuser", "first_name", "last_name", "email", "is_staff", "is_active",  "date_joined",  "profile", "points", "created_at")

# class ProfileSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Profile
#         fields = '__all__'


class CollectiveSerializer(serializers.ModelSerializer):
    class Meta:

        model = Collective
        fields = '__all__'
        # fields = ("name", "blockname", "description", "private", "id_user", "created_at", "members")
        # depth = 1


class MembersOfCollectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembersOfCollective
        fields = '__all__'

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model =  User
        fields = ('id', 'first_name', 'last_name',)