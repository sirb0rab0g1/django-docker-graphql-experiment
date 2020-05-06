from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    BasicInformation,
    Events
)
from rest_framework.validators import UniqueValidator
from django.db import transaction

from rest_framework.response import Response
from django.db.models import Q

class BasicInformationSerializer(serializers.ModelSerializer):
    birth_date = serializers.CharField(required=True, error_messages={'required': 'This field is required'})
    gender = serializers.CharField(required=True, error_messages={'required': 'This field is required'})
    nationality = serializers.CharField(required=True, error_messages={'required': 'This field is required'})
    phone_number = serializers.CharField(required=True, error_messages={'required': 'This field is required'})
    status = serializers.CharField(required=True, error_messages={'required': 'This field is required'})
    address = serializers.CharField(required=True, error_messages={'required': 'This field is required'})
    occupation = serializers.CharField(required=True, error_messages={'required': 'This field is required'})
    company = serializers.CharField(required=True, error_messages={'required': 'This field is required'})

    class Meta:
        model = BasicInformation
        fields = [
            'image',
            'role',
            'birth_date',
            'gender',
            'nationality',
            'phone_number',
            'status',
            'address',
            'creation_date',
            'id'
        ]


class EventsSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True, error_messages={'required': 'This field is required'})
    description = serializers.CharField(required=True, error_messages={'required': 'This field is required'})
    link = serializers.CharField(required=True, error_messages={'required': 'This field is required'})

    class Meta:
        model = Events
        fields = '__all__'

'''
class UserSerializer(serializers.ModelSerializer):
    profile = BasicInformationSerializer()
    # unit = UnitSerializer()
    first_name = serializers.CharField(required=True, error_messages={'required': 'This field is required'})
    last_name = serializers.CharField(required=True, error_messages={'required': 'This field is required'})

    class Meta:
        model = User
        extra_kwargs = {
            'email': {'required': True, 'allow_blank': False, 'validators': [
                UniqueValidator(
                    queryset=User.objects.all(), message='Email already exists.'
                )
            ]},
        }

        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'profile'
            # 'unit'
        )

    @transaction.atomic
    def update(self, instance, validated_data):
        # profile_data = validated_data.pop('profile')

        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()

        if profile_data is not None:
           BasicInformation.objects.filter(id=instance.profile.id).update(**profile_data)

        return instance
'''

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def get_user(self, username_or_email):
        return User.objects.filter(
            Q(username__iexact=username_or_email) | Q(email__iexact=username_or_email)
        ).first()

    def validate_email(self, value):
        if self.get_user(value):
            return value
        else:
            raise serializers.ValidationError('Email does not exist.')

    def validate(self, data):
        user = authenticate(
            username=self.get_user(data['email']).username,
            password=data['password']
        )

        if user is not None:
            return data
        else:
            raise serializers.ValidationError({
                'password': 'Invalid authentication credentials.',
            })

'''
class SignupSerializer(UserSerializer):
    profile = BasicInformationSerializer()

    class Meta:
        model = User
        extra_kwargs = {
            'email': {'required': True, 'allow_blank': False, 'validators': [
                UniqueValidator(
                    queryset=User.objects.all(), lookup='iexact', message='Email already exists.'
                )
            ]},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'write_only': True},
        }
        fields = [
            'id',
            'email',
            'password',
            'first_name',
            'last_name',
            'profile'
        ]


    @transaction.atomic
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User(username=validated_data['email'], **validated_data)
        user.save()
        BasicInformation.objects.create(user=user, **profile_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
'''
