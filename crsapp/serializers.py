from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *

User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims if you want
        token['role'] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add user info to the response
        data.update({
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'role': self.user.role,
        })
        return data





class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'phone',
            'role',
            'is_staff',
            'is_active'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance







class PatientSerializer(serializers.ModelSerializer):
    street = serializers.SlugRelatedField(slug_field='name', queryset=Street.objects.all())
    class Meta:
        model = Patient
        fields = '__all__'
