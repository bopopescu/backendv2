# backend/models/views.py
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from .models import User, Collective, MembersOfCollective, TelegramLog, Plan, Day, Event
from .serializers import UserSerializer, CollectiveSerializer, MembersOfCollectiveSerializer, LoginSerializer, UserFullSerializer,\
    TelegramLogSerializer, PlanSerializer, DaySerializer, EventSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
import json
from datetime import datetime
from datetime import timedelta
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
from . import keyboards
apihelper.proxy = {"https": "socks5://5.133.214.88:39593"}

bot = telebot.TeleBot ("986576341:AAEV01K9Bvi6zqLuwCQP8Vv7QsEngVT0g5k")

from PIL import Image
import base64
import os
# import cv2
# import numpy as np


def requester(token):
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_id FROM authtoken_token WHERE authtoken_token.key = %s", [token])
        row = cursor.fetchone()
        user = User.objects.get(pk=row[0])
        return user



class TelegramLogViewSet(viewsets.ModelViewSet):

    queryset = TelegramLog.objects.all().order_by('-id')
    serializer_class = TelegramLogSerializer

class UserViewSet(viewsets.ModelViewSet):
    # ISSUE exclude password from qs
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
    permission_classes = IsAuthenticated,

    def list(self, request, *args, **kwargs):
        q = User.objects.all().values('id', 'first_name', 'last_name', "status", "is_staff", "points", "profile")
        for g in q:
            print(g)
            # data = UserSerializer.serialize('xml', Som, fields=('name', 'size'))
        n1 = UserFullSerializer(q, many=True)

        json2 = JSONRenderer().render(n1.data)
        print(json2);
        return HttpResponse(json2)
        # jsony = JSONRenderer().render(n1.data)
        # return HttpResponse(jsony)
        # return self.request.user.values('first_name', 'last_name', "status", "is_staff", "points", "profile")



class TelegramViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserFullSerializer
    # permission_classes = IsAuthenticated,
    @api_view(['POST'])
    @bot.message_handler(content_types=["text"])
    def printer(request):


        body_unicode = request.body.decode('utf-8')
        print(body_unicode)

        if ('callback_query' in body_unicode):
            cb = json.loads(body_unicode)["callback_query"]

            if cb["data"]=="logout":
                TelegramLog.objects.filter(chat_id = cb["message"]["chat"]["id"]).delete()
                bot.send_message(cb["message"]["chat"]["id"],
                                 "Logged out from CampAppBot!", reply_markup=keyboards.keyboard_1)
                return HttpResponse("ok")



            if cb["data"] == "rating":
                g1 = User.objects.filter(models.Q(status="4"))
                g1.order_by("points")
                resp = "Рейтинг: \n"
                for user in g1:
                    resp += (user.first_name + " " + user.last_name + " " + user.points + "\n")
                bot.send_message(cb["message"]["chat"]["id"], resp)
                return HttpResponse("ok")

            if cb["data"] == "login":
                g1 = TelegramLog.objects.filter(models.Q(chat_id=cb["message"]["chat"]["id"]))
                if len(g1) ==0:
                    bot.send_message(cb["message"]["chat"]["id"], "You are not logged in. Provide credentials in format\n"
                                     + "Credentials: <LOGIN> <PASSWORD>")
                else:
                    for m in g1:

                        resp = m.t_user.first_name + " " + m.t_user.last_name + "\n" +\
                           "points: " + m.t_user.points +"\n profile: " + m.t_user.profile
                        bot.send_message(cb["message"]["chat"]["id"],
                                     resp, reply_markup=keyboards.keyboard_2)


                return HttpResponse("ok")


        if ('callback_query' not in body_unicode):
            message = json.loads(body_unicode)["message"]
            print(message)


            if message["text"].split(" ")[0] == "Credentials:":
                username = message["text"].split(" ")[1]
                password = message["text"].split(" ")[2]
                print(username + " "+ password)


                user = authenticate(username=username, password=password)
                if user == None:
                    bot.send_message(message["chat"]["id"],
                                 "No such user")
                    return HttpResponse("ok")


                print(user.first_name)
                telegramsession = TelegramLog.objects.update_or_create(chat_id=message["chat"]["id"], t_user = user)

                # telegramsession.save()

                # bot.delete_message(message["chat"]["id"], message["message_id"])


                resp = user.first_name + " " + user.last_name + "\n" + \
                       "points: " + user.points + "\n profile: " + user.profile
                bot.send_message(message["chat"]["id"],
                                 resp, reply_markup=keyboards.keyboard_1)



                return HttpResponse("ok")

            if message["text"] == "/start":
                bot.send_message(message["chat"]["id"],
                                 "Добро пожаловать в CampAppBot!", reply_markup=keyboards.keyboard_1)
                return HttpResponse("ok")










class UserPartialUpdateView(GenericAPIView, UpdateModelMixin):

    queryset =  User.objects.all()
    serializer_class = UserFullSerializer
    permission_classes = IsAuthenticated,

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



class PlanViewSet(viewsets.ViewSet):
    serializer_class = PlanSerializer
    queryset = Plan.objects.all().order_by('-id')

    @api_view(['POST'])
    def create(request):
        print(request.body)
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        start = datetime.strptime(data["start"], '%Y-%m-%dT%H:%M:%S.%fZ')
        end = datetime.strptime(data["end"], '%Y-%m-%dT%H:%M:%S.%fZ')

        print("++++")
        print(start)
        print(end)
        print("++++")
        p1 = Plan(campsession=data["campsession"])
        p1.save()
        p1.refresh_from_db()

        while((end-start).days >=0):

            print(start)
            # d1 = Day(date=str(datetime.strftime(start, '%Y-%m-%d %H:%M:%S')), id_plan=p1)
            # d1 = Day(date=datetime.strftime(start, '%Y-%m-%d %H:%M:%S'), id_plan=p1)
            d1 = Day(date=start, id_plan=p1)
            d1.save()
            start += timedelta(days=1)

        n1 = PlanSerializer(p1)
        json2 = JSONRenderer().render(n1.data)
        return HttpResponse(json2)

    @api_view(['GET'])
    def all(request):
        print(request.body)

        g1 = Plan.objects.all().order_by("id")
        n1 = PlanSerializer(g1, many=True)
        json = JSONRenderer().render(n1.data)

        return HttpResponse(json)


    @api_view(['GET'])
    def get_session_by_day(request, year, month, date):
        d1 = datetime.strptime(year +"/" + month +"/" + date + " 09" , "%Y/%m/%d %H")
        print(d1)

        g1 = Day.objects.filter(date=d1)
        if (len(g1)==0):
            return HttpResponse("no plans for today")
        elif (len(g1)==1):
            plan = g1[0].id_plan
            g2 = Day.objects.filter(id_plan=plan)
            n1 = DaySerializer(g2, many=True)
            json = JSONRenderer().render(n1.data)
            return HttpResponse(json)

        return HttpResponse("LOl")

    def get_session_by_id(request, pk):
        print(pk)

        g2 = Day.objects.filter(id_plan=pk)
        n1 = DaySerializer(g2, many=True)
        json = JSONRenderer().render(n1.data)
        return HttpResponse(json)

    @api_view(['POST'])
    def update_plan(request):
        print(request.body)
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        for day in data:
            d1 = Day.objects.get(pk=day["id"])
            d1.description = day["description"]
            # d1.events.update(day["events"])
            # d1.save()
            d1.events.clear()
            for event in day["events"]:
                print(event)
                e1 = Event.objects.get(name=event["name"])
                d1.events.add(e1)
            d1.save()

            # serializer = DaySerializer(data=day)
            # serializer.is_valid()
            # print(serializer.validated_data)
            # serializer.validated_data.save()
            # d1.save()
        return HttpResponse("hi")



class EventViewSet(viewsets.ViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all().order_by('-id')


    @api_view(['GET'])
    def all(request):
        g1 = Event.objects.filter(base=True).order_by("id")
        n1 = EventSerializer(g1, many=True)
        json = JSONRenderer().render(n1.data)

        return HttpResponse(json)

    @api_view(['POST'])
    def create(request):
        print(request.body)
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)

        e1, created = Event.objects.get_or_create(
            name=data["name"],
        )
        # e1 = Event.(name=data["name"])
        # e1.save()
        e1.refresh_from_db()
        n1 = EventSerializer(e1)
        json2 = JSONRenderer().render(n1.data)

        return HttpResponse(json2)

class ImageProcessViewSet(viewsets.ViewSet):

    @api_view(['POST'])
    def watermark(request):
        # print(request.body)
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        text = (str(data['img']).split("base64")[1])
        image_result = open('camp/assets/dec.jpeg', 'wb')
        image_result.write(base64.b64decode(text))
        image_result.close()

        # image_result.write(base64.b64decode(data['img']))
        base_image = Image.open("camp/assets/dec.jpeg").convert("RGBA")
        watermark = Image.open("camp/assets/logo.png").convert("RGBA")


        width, height = base_image.size
        widthW, heightW = watermark.size

        koef = 5

        newsize = (round(width/koef), round(heightW/(widthW/round(width/koef))))
        watermark = watermark.resize(newsize)
        position = (round(0.98*width-newsize[0]), round(0.98*height-newsize[1]))

        transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        transparent.paste(base_image, (0, 0))
        transparent.paste(watermark, position, mask=watermark)
        # transparent.show()
        transparent.save('camp/assets/done.png')

        with open('camp/assets/done.png', "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        # print(encoded_string);
        # os.remove('camp/assets/done.png')
        # os.remove('camp/assets/dec.jpeg')


        # EXTRA WAY

        # watermark = cv2.imread('camp/assets/logo.png', cv2.IMREAD_UNCHANGED)
        # (wH, wW) = watermark.shape[:2]
        #
        # (B, G, R, A) = cv2.split(watermark)
        # B = cv2.bitwise_and(B, B, mask=A)
        # G = cv2.bitwise_and(G, G, mask=A)
        # R = cv2.bitwise_and(R, R, mask=A)
        # watermark = cv2.merge([B, G, R, A])
        #
        # image = cv2.imread('camp/assets/dec.jpeg')
        # (h, w) = image.shape[:2]
        # image = np.dstack([image, np.ones((h, w), dtype="uint8") * 255])
        #
        #
        # overlay = np.zeros((h, w, 4), dtype="uint8")
        # overlay[h - wH - 10:h - 10, w - wW - 10:w - 10] = watermark
        #
        # # blend the two images together using transparent overlays
        # output = image.copy()
        # cv2.addWeighted(overlay, 1, output, 1.0, 0, output)
        # cv2.imwrite('camp/assets/done.png', output)


        return JsonResponse({"watermarked": "data:image/png;base64,"+ str(encoded_string)})

