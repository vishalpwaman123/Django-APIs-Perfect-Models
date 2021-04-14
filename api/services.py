from django.core.mail import EmailMessage
import os
from decouple import config


class Util:
    Response = None

    @staticmethod
    def send_email(data):
        try:
            print(config("EMAIL_HOST_USER"))
            print(config("EMAIL_HOST_PASSWORD"))
            print(str(data['email_subject'])+" " +
                  str(data['email_body'])+" "+str(data['to_email']))

            email = EmailMessage(subject=data['email_subject'],
                                 body=data['email_body'],
                                 to=[data['to_email']])

            Response = email.send()
            

            return 200

        except Exception:
            # Message = Exception
            # data = {
            #     "status": 500,
            #     "Exception": Message,
            #     "data": data
            # }
            return 500
