from urllib import request
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import *

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email','name', 'surname', 'school', 'password')
        extra_kwargs = {'password':{'write_only':True,'required':True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user

class CreateUserSerializer():
    def create(self, data):
        pass

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        
class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = '__all__'

class RobotControllerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RobotController
        fields = '__all__'