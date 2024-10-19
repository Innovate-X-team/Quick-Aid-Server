import smtplib
import random
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from api.serializers import ConsumerUserSerializer, ProviderUserSerializer, OTPSerializer
from api.models import ConsumerUser, ProviderUser, Otp
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.conf import settings
import sendOtp

# Create your views here.
@api_view(['POST'])
def login(request):
    # Checking user is available or not in both user type
    if('@' in request.data.get('usernameEmail')):
        user = ConsumerUser.objects.filter(email=request.data.get('usernameEmail')).first() or ProviderUser.objects.filter(email=request.data.get('username')).first()
    else:
        user = ConsumerUser.objects.filter(username=request.data.get('usernameEmail')).first() or ProviderUser.objects.filter(username=request.data.get('username')).first()

    if user is None:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    if not user.check_password(request.data.get('password')):
        return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
    serializer = ConsumerUserSerializer(user) if isinstance(user, ConsumerUser) else ProviderUserSerializer(user)
    data = {}
    data["userType"] = "Consumer" if isinstance(user, ConsumerUser) else "Provider"
    data.update({key: dict(serializer.data)[key] for key in ["username", "name", "email", "phone_number"]})
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_user(request):
    if request.data.get('type') == 'consumer':
        serializer = ConsumerUserSerializer(data=request.data)
        print(serializer)
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