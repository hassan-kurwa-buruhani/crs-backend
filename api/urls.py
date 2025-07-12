from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from crsapp.views import *
from rest_framework.routers import DefaultRouter
from crsapp.views import *


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    # JWT token endpoints
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    
    path('', include(router.urls)),
]
