from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from crsapp.views import *
from rest_framework.routers import DefaultRouter
from crsapp.views import *


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'doctor/patients', PatientViewSet, basename='doctor-patients')
router.register(r'sheha/patients', PatientViewSetsheha, basename='sheha-patients')
router.register(r'patients', PatientView, basename='patients')
router.register(r'cases', CaseReportView, basename='cases')


urlpatterns = [
    # JWT token endpoints
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    
    path('', include(router.urls)),
]
