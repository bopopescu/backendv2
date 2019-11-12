# backend/models/views.py
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from .models import User, Collective, MembersOfCollective
from .serializers import UserSerializer, CollectiveSerializer, MembersOfCollectiveSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated
from djoser.permissions import CurrentUserOrAdmin
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
import json
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
    permission_classes = IsAuthenticated,



class UserPartialUpdateView(GenericAPIView, UpdateModelMixin):

    queryset = User.objects.all()
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