from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class EmailResponseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
