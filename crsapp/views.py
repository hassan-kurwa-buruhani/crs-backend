from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer
from rest_framework import generics, permissions
from rest_framework.permissions import IsAdminUser
from .serializers import *
from django.contrib.auth import get_user_model
from rest_framework import viewsets

User = get_user_model()


# Create your views here.
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer




class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
