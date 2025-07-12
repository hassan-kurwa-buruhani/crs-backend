from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from leaflet.admin import LeafletGeoAdmin
from .models import User

from .models import (
    User, Region, District, Street, Sheha,
    HealthCenter, Doctor, Patient, CaseReport, HealthSupervisor
)


# ✅ Custom admin for your custom User model
admin.site.register(User)



# ✅ GeoAdmin for Street (it has PointField)
@admin.register(Street)
class StreetAdmin(LeafletGeoAdmin):
    list_display = ('name', 'district', 'location')
    search_fields = ('name',)
    list_filter = ('district',)



# ✅ Normal admin for Region, District, etc.
@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'region')
    list_filter = ('region',)
    search_fields = ('name',)


@admin.register(Sheha)
class ShehaAdmin(admin.ModelAdmin):
    list_display = ('user', 'street')
    list_filter = ('street', 'user')


@admin.register(HealthCenter)
class HealthCenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'street', 'contact_info')
    search_fields = ('name',)
    list_filter = ('street',)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'health_center')
    list_filter = ('health_center',)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'age', 'gender', 'condition', 'status', 'street')
    list_filter = ('gender', 'condition', 'status', 'street')
    search_fields = ('first_name', 'last_name', 'phone')


@admin.register(CaseReport)
class CaseReportAdmin(admin.ModelAdmin):
    list_display = ('patient', 'health_center', 'doctor', 'date')
    list_filter = ('date', 'health_center', 'doctor')


@admin.register(HealthSupervisor)
class HealthSupervisorAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'email')
    search_fields = ('user__first_name', 'user__last_name', 'email')
