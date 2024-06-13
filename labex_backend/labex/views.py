import json
import random
import requests
from .models import *
from calendar import c
from .serializers import *
from distutils import command
from sqlite3 import paramstyle
from datetime import date, datetime
from .configs import labex_config as cf
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, serializers, permissions, generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


'''

    Robot controller section

'''
@api_view(['GET'])
def get_controller_name_by_controller_id(request):
    controller_id = ''

    try:
        controller_id = request.data['controller_id']
    except Exception as e: 
        print('error : ', e)

    return RobotController.objects.get(controller_id=controller_id)

def update_command_by_controller_id(controller_id, command):
    robot_info = RobotController.objects.get(controller_id=controller_id)
    robot_info.lastest_command = command
    robot_info.save()
    return robot_info

def update_controller_by_controller_id(controller_id, controller_name):
    robot_info = RobotController.objects.get(controller_id=controller_id)
    robot_info.controller_name = controller_name
    robot_info.save()
    return robot_info

def initial_robot():
    for i in range(3):
        robot = RobotController.objects.create(controller_name='-', lastest_command="-")
        robot.save()


@api_view(['POST'])
def change_controller(request):
    if len(RobotController.objects.all()) == 0:
        initial_robot()
        
    controller_id = request.data['controller_id']
    controller_name = request.data['controller_name']
    url = cf.robot_config_url['controller' + controller_id]
    headers = {
        'x-api-key' : cf.post_controller
    }
    param = {
        'auth': controller_name
    }
    response = requests.request(
        "POST", url=url, data=param, headers=headers)
    response_json = response.json()
    if response.status_code == 200:
        update_controller_by_controller_id(controller_id, response_json['auth'])

    try:
        robot_info = RobotController.objects.get(controller_id=controller_id)
    except Exception as e:
        return Response({'status': '400', 'detail':str(e)}, status=200)

    serializer = RobotControllerSerializer(robot_info)
    response = serializer.data
    return Response(response ,status=200)

@api_view(['POST'])
def change_command(request):
    controller_id = request.data['controller_id']
    controller_name = request.data['controller_name']
    command = request.data['command']

    url = cf.robot_config_url['command_robot' + controller_id]
    headers = {
        'x-api-key' : cf.post_command
    }
    param = {
        'auth': controller_name,
        'command' : command
    }
    response = requests.request(
        "POST", url=url, data=param, headers=headers)
    print(response.status_code)

    if response.status_code == 200:
        update_command_by_controller_id(controller_id, command)

    return Response(response.status_code)

'''

Authen User Section

'''

@api_view(['GET'] )
def login(request):
    email = request.data['email']
    password = request.data['password']
    print('test')
    try:
        user_object = User.objects.get(email=email, password=password)

        if user_object == None:
            return Response({'status': '400', 'detail':str(e)}, status=400)
        print(user_object)
        serializer = UserSerializer(user_object)        
        response = serializer.data
    except Exception as e: 
        return Response({'status': '400', 'detail':str(e)}, status=400)

    return Response(response ,status=200)

'''

    Lab section

'''
class LabViewset(viewsets.ModelViewSet):

    queryset = Lab.objects.all().order_by('lab_id')
    serializer_class = LabSerializer

    # Create lab
    def create(self, request):
        lab_object = Lab.objects.create()
        try:
            print(request.data)
            lab_object.lab_name = "Robot Controller Lab"
            lab_object.code = request.data['code']
            # lab_object.date_time_slot = date.today
            lab_object.robot = RobotController.objects.filter(controller_id=request.data['robot']).last()
            lab_object.user_controller = User.objects.filter(email=request.data['user']).last()
            lab_object.save()
        except Exception as e:
            lab_object = None
            print(f'Create lab error {e}')

        serializer = LabSerializer(lab_object)
        response = serializer.data
        return Response(response ,status=200)

    @action(detail=False, methods=['post'], url_path='validate_labcode')
    def validate_lab_code(self, request):
        code = request.data['lab_code']
        
        try:
            lab_object = Lab.objects.filter(code=code).last()
        except Exception as e:
            return Response({'status': '400', 'detail':str(e)}, status=400)

        if lab_object:
            serializer = LabSerializer(lab_object)        
            response = serializer.data
            return Response(response ,status=200)
        else: 
            return Response(status=400)

    def generate_lab_code(lab_object):
        code = random.randint(1000,9999)
        lab_object.code = code
        lab_object.save()
        print(f'updated lab {lab_object.lab_id} code!')
        return lab_object

    def check_lab_expired_date(self, lab_object):
        today = date.today()

        if lab_object.expire_date == today:
            self.generate_lab_code(lab_object.lab_id)
            print('Re generate lab code')

'''

    User section

'''
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('user_id')
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )    
    # # Sign Up
    # def create(self, request):
    #     user_object = User.objects.create()
    #     try:
    #         user_object.email = request.data['email']
    #         user_object.name = request.data['name']
    #         user_object.surname = request.data['surname']
    #         user_object.school = request.data['school']
    #         user_object.DOB = request.data['DOB']
    #         user_object.password = request.data['password']
    #         user_object.role = "student"
    #         user_object.save()
    #     except Exception as e:
    #         user_object = None
    #         print(f'Create user error {e}')

    #     serializer = RobotControllerSerializer(user_object)
    #     response = serializer.data
    #     return Response(response ,status=200)

class AppointmentViewSet(   viewsets.ModelViewSet):
    queryset = Appointment.objects.all().order_by('appointment_id')
    serializer_class = AppointmentSerializer

    def create(self, request):
        email = request.data['email'] 
        lab_code = request.data ['lab_code']

        appointment_object = Appointment.objects.create()
        try:
            appointment_object.user = self.get_user_email(email)
        except:
            print('cannot get user')

        try:
            appointment_object.lab_code = self.get_lab_code(lab_code)
        except:
            print('cannot get lab code')

        appointment_object.save()

        return appointment_object