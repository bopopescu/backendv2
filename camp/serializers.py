# backend/models/serializers.py
from rest_framework import serializers
from .models import User, Collective, MembersOfCollective



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

# class ProfileSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Profile
#         fields = '__all__'


class CollectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collective
        fields = '__all__'


class MembersOfCollectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembersOfCollective
        fields = '__all__'

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'name', 'surname',)