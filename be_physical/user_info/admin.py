from django.contrib import admin

from .models import UserAnnotation, UserInfo, UserTrackingPoint

# Register your models here.
admin.site.register([UserInfo, UserAnnotation, UserTrackingPoint])
