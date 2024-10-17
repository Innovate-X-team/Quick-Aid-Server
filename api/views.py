import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from api.serializers import ConsumerUserSerializer, ProviderUserSerializer, OTPSerializer
from api.models import ConsumerUser, ProviderUser, Otp
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.conf import settings


# Create your views here.
@api_view(['POST'])
def login(request):
    # Checking user is available or not in both user type
    user = ConsumerUser.objects.filter(username=request.data.get('username')).first() or ProviderUser.objects.filter(username=request.data.get('username')).first()
    if user is None:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    if user.password != request.data.get('password'):
        return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
    serializer = ConsumerUserSerializer(user) if isinstance(user, ConsumerUser) else ProviderUserSerializer(user)
    data = {}
    data["userType"] = "Consumer" if isinstance(user, ConsumerUser) else "Provider"
    data.update({key: dict(serializer.data)[key] for key in ["username", "name", "email", "phone_number"]})
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_user(request):
    if request.data.get('userType') == 'Consumer':
        serializer = ConsumerUserSerializer(data=request.data)
    else:
        serializer = ProviderUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def verify_email(request):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("sayanbiswas6073@gmail.com", settings.EMAIL_PASSWORD)
    code = int(''.join(str(random.randint(0, 9)) for _ in range(6)))
    Otp.objects.filter(email=request.data.get('email')).delete()  # Deleting previous OTP if exists
    Otp.objects.create(email=request.data.get('email'), otp=code)
    msg = MIMEMultipart("alternative")
    msg["subject"] = "Verify Email"
    msg["From"] = "sayanbiswas6073@gmail.com"
    msg["To"] = request.data.get('email')
    html_content = f"""
        <html>
            <body>
                <h1>Verify Your Email</h1>
                <p>Your verification code is: <strong>{code}</strong></p>
                <p>Please enter this code in the Quick Aid app to complete the registration process.</p>
            </body>
        </html>
    """
    msg.attach(MIMEText(html_content, "html"))

    s.send_message(msg)
    s.quit()
    return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)