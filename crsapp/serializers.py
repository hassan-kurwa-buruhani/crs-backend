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


class CaseSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    health_center = serializers.SlugRelatedField(
        slug_field='name',
        queryset=HealthCenter.objects.all()
    )
    doctor = serializers.SlugRelatedField(
        slug_field='user__first_name',
        queryset=Doctor.objects.all()
    )
    district = serializers.SerializerMethodField()
    street_name = serializers.SerializerMethodField()
    street_location = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()
    doctor_full_name = serializers.SerializerMethodField()

    def get_doctor_full_name(self, obj):
        return f"{obj.doctor.user.first_name} {obj.doctor.user.last_name}"

    def get_district(self, obj):
        return obj.patient.street.district.name

    def get_region(self, obj):
        return obj.patient.street.district.region.name

    def get_street_name(self, obj):
        return obj.patient.street.name

    def get_street_location(self, obj):
        location = obj.patient.street.location
        if location:
            return {
                "latitude": location.y,
                "longitude": location.x
            }
        return None

    class Meta:
        model = CaseReport
        fields = '__all__'
        

