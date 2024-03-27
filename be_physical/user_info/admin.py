from django.contrib import admin
from django.db import models

from .models import UserAnnotation, UserInfo, UserTrackingLabel, UserTrackingPoint


class UserAnnotationInline(admin.TabularInline[UserAnnotation, models.Model]):
    model = UserAnnotation
    extra = 0


class UserTrackingPointInline(admin.TabularInline[UserTrackingPoint, models.Model]):
    model = UserTrackingPoint
    extra = 0
    ordering = ["label", "-date"]


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin[UserInfo]):
    search_fields = ["user__username"]
    inlines = [UserAnnotationInline, UserTrackingPointInline]
    readonly_fields = ["bmi", "bmi_category"]
    list_display = ["user", "height", "birth_date", "bmi", "bmi_category"]
    list_filter = ["user", "height", "birth_date"]


@admin.register(UserAnnotation)
class UserAnnotationAdmin(admin.ModelAdmin[UserAnnotation]):
    list_display = ["user_info", "text", "annotation_type", "scope", "status"]
    list_filter = ["user_info", "annotation_type", "scope", "status"]
    search_fields = ["user_info", "text"]


@admin.register(UserTrackingPoint)
class UserTrackingPointAdmin(admin.ModelAdmin[UserTrackingPoint]):
    list_display = ["user_info", "label", "date", "value"]
    list_filter = ["user_info", "label", "date"]
    search_fields = ["user_info", "label"]


@admin.register(UserTrackingLabel)
class UserTrackingLabelAdmin(admin.ModelAdmin[UserTrackingLabel]):
    list_display = ["label", "description"]
    list_filter = ["label"]
    search_fields = ["label", "description"]
