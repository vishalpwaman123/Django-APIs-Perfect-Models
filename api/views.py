from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status, generics, views
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
import json
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import User
from .validation import RegisterView_Validation, SendEmail_Validation
from .serializers import UserSerializer, EmailResponseSerializer, EmailAccountVarificationSerializer, UserDetail
from .services import Util, RetriveAttribute

# Create your views here.


class RegisterView(GenericAPIView):

    serializer_class = UserSerializer

    def post(self, request):

        print("flag 1")

        Validation_data = RegisterView_Validation(request)
        if Validation_data:
            return Response(Validation_data, status=status.HTTP_400_BAD_REQUEST)

        print("flag 2")
        try:
            print("flag 3")
            emaildata = User.objects.get(email=request.data.get("email"))
            print("flag 4", emaildata)
            if emaildata:
                Message = "Email Is already in used"
                data = {
                    "Message": Message,
                    "data": request.data
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except:
            pass

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            Message = "Success"
            data = {
                "Message": Message,
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)

        Message = "Failed"
        data = {
            "Message": Message,
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)


class SendEmailView(GenericAPIView):

    serializer_class = EmailResponseSerializer

    def post(self, request):
        # print("flag 1")
        Validation_response = SendEmail_Validation(request)
        if Validation_response:
            return Response(Validation_response, status=status.HTTP_400_BAD_REQUEST)
        try:
            email_Response = User.objects.get(email=request.data.get("email"))
            print(email_Response)
        except:
            Message = "Email Id Does Not Found, Enter Valid Email Id"
            return Response(Message, status=status.HTTP_400_BAD_REQUEST)

        print("data:", email_Response)
        # payload = {"email": str(email_Response)}
        # print(payload)
        # token = jwt.encode(payload, settings.SECRET_KEY)
        token = RefreshToken.for_user(email_Response).access_token

        current_site = get_current_site(request).domain

        absoluteUrl = 'http://'+current_site + \
            "/api/varify_email/?token="+str(token)
        email_body = "Hi " + email_Response.first_name + \
            " Use link below to verify Account :\n"+absoluteUrl
        data = {"email_body": email_body, 'to_email': email_Response.email,
                'email_subject': 'Verify Your Account'}
        Email_Response = Util.send_email(data)
        print(Email_Response)
        if Email_Response == 200:
            Message = "Email Send SucessFully"
            data = {
                "Message": Message,
                "data": data
            }
            print("status mail 200")
            return Response(data, status=status.HTTP_200_OK)
        else:
            Message = "Email Send Unsucessfully"
            data = {
                "Message": Message,
                "data": data
            }
            print("Status mail 500")
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyEmail(views.APIView):

    serializer_class = EmailAccountVarificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, options={"verify_signature": False})

            data = User.objects.get(id=payload['user_id'])
            if not data.is_verified:
                data.is_verified = True
                print("User is_verified 1 =", data.is_verified)
                data.save()
                serializer = UserDetail(data, many=False)
                Message = "User Account Varification"
                data = {
                    "Message": Message,
                    "data": serializer.data
                }
                print("Response :", data)
                return Response(data, status=status.HTTP_200_OK)
            else:
                Message = "Account Already Varified"
                serializer = UserDetail(data, many=False)
                data = {
                    "Message": Message,
                    "data": serializer.data
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError as identifier:
            data = {
                "Error": "JWT Signature Error"
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            data = {
                "Error": "Jwt Decode Token Error"
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
