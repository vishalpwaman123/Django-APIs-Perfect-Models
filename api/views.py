from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import json

from .models import User
from .validation import RegisterView_Validation, SendEmail_Validation
from .serializers import UserSerializer, EmailResponseSerializer
from .services import Util

# Create your views here.


class RegisterView(GenericAPIView):

    def post(self, request):

        Validation_data = RegisterView_Validation(request)
        if Validation_data:
            return Response(Validation_data, status=status.HTTP_400_BAD_REQUEST)

        try:
            emaildata = User.objects.get(email=request.data.get("email"))
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

    def post(self, request):
        print("flag 1")
        Validation_response = SendEmail_Validation(request)
        if Validation_response:
            return Response(Validation_response, status=status.HTTP_400_BAD_REQUEST)

        print("flag 2")
        try:
            email_Response = User.objects.get(email=request.data.get("email"))
        except email_Response.DoesNotExist:
            Message = "Email Id Does Not Found, Enter Valid Email Id"
            return Response("Message", status=status.HTTP_400_BAD_REQUEST)

        token = RefreshToken.for_user(email_Response).access_token

        current_site = get_current_site(request).domain
        # relativeLink = reverse('api:email-verify') + relativeLink
        # print(relativeLink)
        absoluteUrl = 'http://'+current_site+"?token="+str(token)
        email_body = "Hi " + email_Response.first_name + \
            " Use link below to verify Account :\n"+absoluteUrl
        data = {"email_body": email_body, 'to_email': email_Response.email,
                'email_subject': 'Verify Your Account'}
        Email_Response = Util.send_email(data)
        # serializer = EmailResponseSerializer(data=Email_Response)
        # result = json.dumps(Email_Response)
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

        # Message = "Email Sending Failed"
        # data = {
        #     "Message": Message,
        #     "data": email_Response
        # }
        # return Response(data, status=status.HTTP_400_BAD_REQUEST)
