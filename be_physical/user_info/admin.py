from django.contrib import admin

from .models import UserAnnotation, UserInfo, UserTrackingLabel, UserTrackingPoint

# Register your models here.


class UserAnnotationInline(admin.TabularInline):  # type: ignore
    model = UserAnnotation
    extra = 0


class UserTrackingPointInline(admin.TabularInline):  # type: ignore
    model = UserTrackingPoint
    extra = 0
    ordering = ["label", "-date"]


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin[UserInfo]):
    search_fields = ["user_id__username"]
    inlines = [UserAnnotationInline, UserTrackingPointInline]
    readonly_fields = ["bmi", "category_name_by_bmi"]
    list_display = ["user_id", "height", "birth_date", "bmi", "category_name_by_bmi"]
    list_filter = ["user_id", "height", "birth_date"]


@admin.register(UserAnnotation)
class UserAnnotationAdmin(admin.ModelAdmin[UserAnnotation]):
    list_display = ["user_id", "text", "annotation_type", "scope", "status"]
    list_filter = ["user_id", "annotation_type", "scope", "status"]
    search_fields = ["user_id", "text"]


@admin.register(UserTrackingPoint)
class UserTrackingPointAdmin(admin.ModelAdmin[UserTrackingPoint]):
    list_display = ["user_id", "label", "date", "value"]
    list_filter = ["user_id", "label", "date"]
    search_fields = ["user_id", "label"]


@admin.register(UserTrackingLabel)
class UserTrackingLabelAdmin(admin.ModelAdmin[UserTrackingLabel]):
    list_display = ["label", "description"]
    list_filter = ["label"]
    search_fields = ["label", "description"]
