from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from leaflet.admin import LeafletGeoAdmin
from .models import User

from .models import (
    User, Region, District, Street, Sheha,
    HealthCenter, Doctor, Patient, CaseReport
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
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'patient':
            # Exclude Patients that already have a CaseReport
            used_patients = CaseReport.objects.values_list('patient', flat=True)
            kwargs['queryset'] = Patient.objects.exclude(id__in=used_patients)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    list_display = ('patient', 'health_center', 'doctor', 'date')
    list_filter = ('date', 'health_center', 'doctor')


