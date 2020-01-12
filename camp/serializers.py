# backend/models/serializers.py
from rest_framework import serializers
from .models import User, Collective, MembersOfCollective, TelegramLog, Plan, Event, Day
from django.conf import settings



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class TelegramLogSerializer(serializers.ModelSerializer):
    class Meta:
        model =  TelegramLog
        fields = '__all__'

class UserFullSerializer(serializers.ModelSerializer):
    class Meta:
        # model =  settings.AUTH_USER_MODEL
        model = User
        fields = ('id', 'first_name', 'last_name', "status", "points", "profile")
        # fields = ("id", "is_superuser", "first_name", "last_name", "email", "is_staff", "is_active",  "date_joined",  "profile", "points", "created_at")

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = '__all__'
        depth = 1


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
        model =  User
        fields = ('id', 'first_name', 'last_name',)