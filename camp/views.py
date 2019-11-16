# backend/models/views.py
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from .models import User, Collective, MembersOfCollective
from .serializers import UserSerializer, CollectiveSerializer, MembersOfCollectiveSerializer, LoginSerializer, UserFullSerializer
from rest_framework.permissions import IsAuthenticated
from djoser.permissions import CurrentUserOrAdmin
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
import json
from django.conf import settings
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from django.db import connection
from django.db import models
from rest_framework.renderers import JSONRenderer
import telebot
from telebot import apihelper
apihelper.proxy = {"https": "socks5://167.86.121.208:40194"}

bot = telebot.TeleBot ("986576341:AAEKIUXGsEj2kLs4DK_JHRMRdg4O6F7fUo4")


def requester(token):
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_id FROM authtoken_token WHERE authtoken_token.key = %s", [token])
        row = cursor.fetchone()
        user = User.objects.get(pk=row[0])
        return user




class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
    permission_classes = IsAuthenticated,





class TelegramViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserFullSerializer
    # permission_classes = IsAuthenticated,
    @api_view(['POST'])
    def printer(request):
        body_unicode = request.body.decode('utf-8')
        message = json.loads(body_unicode)["message"]
        print(message)
        g1 = User.objects.filter(models.Q(status="4"))
        g1.order_by("points")
        # g1 = User.objects.all()
        resp =""
        for user in g1:
            resp+=(user.first_name+ " " + user.last_name + " "+ user.points + "\n")

        if message["text"] == "hi":
            bot.send_message(message["chat"]["id"], resp)
        return HttpResponse ("ok")





class UserPartialUpdateView(GenericAPIView, UpdateModelMixin):

    queryset =  User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = CurrentUserOrAdmin

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @api_view(['POST'])
    def group_points_update(request):
        print(request.body)
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        print(data)
        to_upd = User.objects.filter(id__in=data["members"])
        for user in to_upd:
            user.points = str(int(user.points) + int(data["amount"]))
            print(str(int(user.points) + int(data["amount"])))
            user.save()
        return JsonResponse({"message": "OK"})




class CollectiveViewSet(viewsets.ModelViewSet):
    queryset = Collective.objects.all().order_by('-id')
    serializer_class = CollectiveSerializer
    # permission_classes = (IsAuthenticated, IsAdminUser)
    @api_view(['POST'])
    def new_collective(request):
        print(request.headers)
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode);
        token = request.headers["Authorization"].split()[1]
        creator = requester(token)
        col = Collective(name= data["name"], blockname=data["blockname"], description=data["description"], private=data["private"], id_user=creator)
        col.save()
        col.refresh_from_db()
        for id in data["members"]:
            us = User.objects.get(pk=id)
            col.members.add(us)

        return JsonResponse({"id_creator": creator.id, "obj": col.id,"created_at": col.created_at})

    @api_view(['GET'])
    def my_collectives(request):
        print("jkik")
        token = request.headers["Authorization"].split()[1]
        user = requester(token)
        g1 = Collective.objects.filter(models.Q(id_user=user) | models.Q(private=False))
        n1 = CollectiveSerializer(g1, many=True)
        json = JSONRenderer().render(n1.data)
        return HttpResponse(json)


class MembersOfCollectiveViewSet(viewsets.ModelViewSet):
    queryset = MembersOfCollective.objects.all().order_by('-id')
    serializer_class = MembersOfCollectiveSerializer
    # permission_classes = (IsAuthenticated, IsAdminUser)



# class LoginViewSet(viewsets.ModelViewSet):
#     serializer_class = UserSerializer
#     queryset = User.objects.all().order_by('-id')


class LoginViewSet(viewsets.ViewSet):
    serializer_class = LoginSerializer
    queryset = User.objects.all().order_by('-id')

    @action(detail=False, methods=['post'])
    @csrf_exempt
    def auth(self, request):
        print(request.body)
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        user = authenticate(username=data["username"], password= data["password"])
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse('Authenticated successfully')
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')

        # return Response({'Hello': 'World'})