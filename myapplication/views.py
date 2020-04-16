from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from django.db import transaction
from rest_framework import (
    status,
    views,
    viewsets
)
from django.contrib.auth.password_validation import validate_password
from .models import (
    BasicInformation,
    Events
)

from .serializers import (
    UserSerializer,
    EventsSerializer,
    LoginSerializer,
    SignupSerializer
)
from django.contrib.auth.models import User
from api.utils import generate_jwt_token

from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser, JSONParser
from rest_framework.exceptions import ParseError
import json

from rest_framework.decorators import (
    api_view,
    action,
    authentication_classes,
    permission_classes
)

# image upload
from django.core.files.base import ContentFile
import base64

#email sending
from .sendemail import *
from django.core import serializers

from datetime import datetime, timedelta
import pytz

#for ws
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def jwt_response_payload_handler(token, uto_emailser=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user).data
    }


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class EventsViewSet(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer

    def create(self, request, format=None):
        data = request.data.copy()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        layer = get_channel_layer()
        serializer.save()

        async_to_sync(layer.group_send)('events', {
            'type': 'events.alarm',
            'content': serializer.data
        })

        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def send_reset_password(request):
    try:
        user = User.objects.get(email=request.data['email'])
        domain_name = '{}/resetpassword?token={}'.format(
            request.data.get('domain_name'),
            generate_jwt_token(user)
        )
        sendemail(user.email, domain_name)
        return Response({'success': True}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({
            'email': [
                'Email does not exist.'
            ]}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def save_new_password(request):
    password = request.data.get('password')

    try:
        validate_password(password)
    except Exception as e:
        return Response({
            're_password': e.messages,
        }, status=status.HTTP_400_BAD_REQUEST)

    request.user.set_password(password)
    request.user.save()
    return Response({
        'success': True,
    }, status=status.HTTP_202_ACCEPTED)

class LoginViewSet(views.APIView):
    serializer_class = LoginSerializer
    permission_classes = [
        AllowAny,
    ]

    def post(self, request, format=None):
        data = request.data.copy()
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            user = serializer.get_user(data['email'])
            return Response({
                'user': UserSerializer(user).data,
                'token': generate_jwt_token(user)
            })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupViewSet(CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [
        AllowAny,
    ]

    def post(self, request, format=None):
        data = request.data.copy()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'token': generate_jwt_token(user),
            'user': UserSerializer(user).data,
        })
