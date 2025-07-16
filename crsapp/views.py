from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer
from rest_framework import generics, permissions, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import *
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .models import *


User = get_user_model()


# Create your views here.
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer




class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]




# doctor-patients view
class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Make sure this user is a doctor
        try:
            doctor = Doctor.objects.get(user=user)
        except Doctor.DoesNotExist:
            return user  # Return empty queryset if not a doctor

        health_center = doctor.health_center

        # Return patients linked to this health center through CaseReports
        return Patient.objects.filter(
            casereport__health_center=health_center
        ).distinct()


class PatientViewSetsheha(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Make sure this user is a doctor
        try:
            sheha = Sheha.objects.get(user=user)
        except Sheha.DoesNotExist:
            return []  # Return empty queryset if not a doctor

        street = sheha.street

        # Return patients linked to this health center through CaseReports
        return Patient.objects.filter(
            street=street
        ).distinct()
    

class PatientView(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()
    permission_classes = [permissions.IsAuthenticated]

class CaseReportView(viewsets.ModelViewSet):
    serializer_class = CaseSerializer
    queryset = CaseReport.objects.all()
    permission_classes = [permissions.IsAuthenticated]