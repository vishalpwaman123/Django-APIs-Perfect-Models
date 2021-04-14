from django.urls import path
from .views import RegisterView, SendEmailView

app_name = 'api'

urlpatterns = [
    path('register/', RegisterView.as_view(), name="Registration"),
    path('send_email/', SendEmailView.as_view(), name="Send Email")
]
