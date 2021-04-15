from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']


class UserDetail(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class EmailResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class EmailAccountVarificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'email', 'password', 'is_verified']

