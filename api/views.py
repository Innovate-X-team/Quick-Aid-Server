import os
import smtplib
import random
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from api.serializers import ConsumerUserSerializer, ProviderUserSerializer, TaskSerializer, OTPSerializer
from api.models import ConsumerUser, ProviderUser, Task, Otp
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.conf import settings
from geopy.geocoders import Nominatim
import firebase_admin
from firebase_admin import messaging
from firebase_admin import credentials
import json
from .sendOtp import sendOTP
from .haversine import haversine, two_point_distance

cred = credentials.Certificate(os.path.join('serviceAccountKey.json'))
default_app = firebase_admin.initialize_app(cred)

# Create your views here.
@api_view(['POST'])
def login(request):
    # Checking user is available or not in both user type
    if('@' in request.data.get('usernameEmail')):
        user = ConsumerUser.objects.filter(email=request.data.get('usernameEmail')).first() or ProviderUser.objects.filter(email=request.data.get('usernameEmail')).first()
    else:
        user = ConsumerUser.objects.filter(username=request.data.get('usernameEmail')).first() or ProviderUser.objects.filter(username=request.data.get('usernameEmail')).first()

    if user is None:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    if not user.check_password(request.data.get('password')):
        return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
    
    user.device_token = request.data.get('token')
    user.save()
    serializer = ConsumerUserSerializer(user) if isinstance(user, ConsumerUser) else ProviderUserSerializer(user)
    data = {}
    data["userType"] = "Consumer" if isinstance(user, ConsumerUser) else "Provider"
    data.update({key: dict(serializer.data)[key] for key in ["username", "name", "email", "phone_number"]})
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_user(request):
    if request.data.get('type') == 'consumer':
        serializer = ConsumerUserSerializer(data=request.data)
    else:
        serializer = ProviderUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def send_email_otp(request):
    email = request.data.get('email')
    name = request.data.get('name')
    if request.data.get('type') == 'change':
        if('@' in request.data.get('usernameEmail')):
            user = ConsumerUser.objects.filter(email=request.data.get('usernameEmail')).first() or ProviderUser.objects.filter(email=request.data.get('usernameEmail')).first()
        else:
            user = ConsumerUser.objects.filter(username=request.data.get('usernameEmail')).first() or ProviderUser.objects.filter(username=request.data.get('usernameEmail')).first()
        if user:
            email = user.email
            name = user.name
        else:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    code = str(random.randint(1, 9))
    code = int(code + ''.join(str(random.randint(0, 9)) for _ in range(5)))
    
    Otp.objects.filter(email=email).delete()  # Deleting previous OTP if exists
    Otp.objects.create(email=email, otp=code)
    sendOTP(request.data.get('type'), name, email, code)
    return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def verify_email(request):
    email = request.data.get('email')
    if request.data.get('usernameEmail'):
        if '@' in request.data.get('usernameEmail'):
            email = request.data.get('usernameEmail')
        else:
            email = ConsumerUser.objects.filter(username=request.data.get('usernameEmail')).first().email or ProviderUser.objects.filter(username=request.data.get('usernameEmail')).first().email
    otp = Otp.objects.filter(email=email).first()
    if int(request.data.get('otp')) == otp.otp:
        # checking if otp is older then 10 minuts or not
        if ((otp.created_at + datetime.timedelta(minutes=10))).timestamp() >= datetime.datetime.now().timestamp():
            otp.delete()
            return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        otp.delete()
        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def change_password(request):
    if request.data.get('usernameEmail'):
        if '@' in request.data.get('usernameEmail'):
            email = request.data.get('usernameEmail')
        else:
            email = ConsumerUser.objects.filter(username=request.data.get('usernameEmail')).first().email or ProviderUser.objects.filter(username=request.data.get('usernameEmail')).first().email
    else:
        return Response({"error": "Email or username not provided"}, status=status.HTTP_400_BAD_REQUEST)
    
    user = ConsumerUser.objects.filter(email=email).first() or ProviderUser.objects.filter(email=email).first()
    user.set_password(request.data.get('password'))
    user.save()
    return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def check_username(request):
    username = request.data.get('username')
    if ConsumerUser.objects.filter(username=username).exists() or ProviderUser.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Username available"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_location(request):
    # update location of provider user
    user = ProviderUser.objects.filter(username=request.data.get('username')).first()
    if user:
        user.current_lat = request.data.get('latitude')
        user.current_lon = request.data.get('longitude')
        user.save()
    else:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # send notification to consumer user

    return Response({"message": "Location updated successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def onduty_toggle(request):
    user = ProviderUser.objects.filter(username=request.data.get('username')).first()
    if user:
        user.on_duty = request.data.get('on_duty')
        user.save()
        return Response({"message": "Duty status updated successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def is_onduty(request):
    user = ProviderUser.objects.filter(username=request.data.get('username')).first()
    if user:
        return Response({"on_duty": user.on_duty}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def call_service(request):
    geolocator = Nominatim(user_agent="quickaid")
    location = geolocator.reverse((request.data.get('latitude'), request.data.get('longitude')), 
    exactly_one=True)
    
    if "city" in location.raw["address"]:
        ambulance_provider = ProviderUser.objects.filter(on_duty=True, on_work=False, city=location.raw['address']["city"], service_type=request.data.get('type')).all()
    else:
        ambulance_provider = ProviderUser.objects.filter(on_duty=True, on_work=False, district=location.raw['address']["state_district"], service_type=request.data.get('type')).all()

    user = ConsumerUser.objects.filter(username=request.data.get('username')).first()
    task = TaskSerializer(data={
        'consumer': user.id,
        'task_type': request.data.get('type'),
        'latitude' : request.data.get('latitude'),
        'longitude' : request.data.get('longitude'),
        'location_name': str(location),
        'status': 'Pending'
    })
    if task.is_valid():
        task = task.save()
        user.service_request = task
        task.save
        user.save()

    ambulance_provider_serializer = ProviderUserSerializer(ambulance_provider, many=True)

    lat1 = request.data.get('latitude')
    lon1 = request.data.get('longitude')
    distance = []
    for provider in ambulance_provider_serializer.data:
        providerUser = ProviderUser.objects.filter(username=provider['username']).first()
        providerUser.task_assigned = task
        providerUser.save()
        distance.append({
            'username': provider['username'],
            'distance': two_point_distance(lat1, lon1, provider['current_lat'], provider['current_lon']),
            'token': provider['device_token']
        })
    
    sorted_provider = sorted(distance, key=lambda item: item['distance'])
    

    # sending notification to service providers
    if len(sorted_provider) == 0:
        return Response({"message": "No Provider available"}, status=status.HTTP_404_NOT_FOUND)
    elif len(sorted_provider) <= 10:
        pass
    else:
        sorted_provider = sorted_provider[:10]


    for provider in list(map(lambda d: [d['username'], d['token']], sorted_provider)):
        notification_message = messaging.Message(
            token=provider[1],
            # notification= messaging.Notification(
            #     title = 'New Task Available',
            #     body = f"New task available at {str(location)}",
            # ),
            data = {
                'title': 'New Task Available',
                'body': f"New task available at {str(location)}",
                'latitude': str(lat1),
                'longitude': str(lon1),
                'username': str(provider[0]),
                'task_id': str(task.id)
            },
        )
        response = messaging.send(notification_message)

    

    return Response({"message": "Service requested successfully", "data": ambulance_provider_serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def get_assigned_task(request):
    user = ProviderUser.objects.filter(username=request.data.get('username')).first()
    if user:
        task = user.task_assigned
        if task:
            return Response({"message": "Task found", "data": {
                'consumer': {
                    'username': user.task_assigned.consumer.username,
                    'name': user.task_assigned.consumer.name,
                    'phone_number': user.task_assigned.consumer.phone_number
                },
                'task': TaskSerializer(task).data,
                'distance': two_point_distance(user.current_lat, user.current_lon, task.latitude, task.longitude)
            }}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No task assigned"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def accept_task(request):
    task = Task.objects.filter(id=request.data.get('task_id')).first()
    if task.provider:
        return Response({"message": "Task already accepted"}, status=status.HTTP_400_BAD_REQUEST)
    provider = ProviderUser.objects.filter(username=request.data.get('username')).first()
    task.provider = provider
    task.save()
    provider.on_work = True
    provider.save()
    return Response({"message": "Task accepted"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def complete_task(request):
    task = Task.objects.filter(id=request.data.get('task_id')).first()
    provider = task.provider
    provider.on_work = False
    provider.save()
    task.delete()
    return Response({"message": "Task completed"}, status=status.HTTP_200_OK)
