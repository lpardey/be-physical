from django.contrib import admin

from .models import UserAnnotation, UserInfo, UserTrackingLabel, UserTrackingPoint

# Register your models here.


class UserAnnotationInline(admin.TabularInline):
    model = UserAnnotation
    extra = 0


class UserTrackingPointInline(admin.TabularInline):
    model = UserTrackingPoint
    extra = 0
    ordering = ["label", "-date"]


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    search_fields = ["user_id__username"]
    inlines = [UserAnnotationInline, UserTrackingPointInline]
    readonly_fields = ["bmi", "category_name_by_bmi"]
    list_display = ["user_id", "height", "birth_date", "bmi", "category_name_by_bmi"]
    list_filter = ["user_id", "height", "birth_date"]


@admin.register(UserAnnotation)
class UserAnnotationAdmin(admin.ModelAdmin):
    list_display = ["user_id", "text", "annotation_type", "scope", "status"]
    list_filter = ["user_id", "annotation_type", "scope", "status"]
    search_fields = ["user_id", "text"]


@admin.register(UserTrackingPoint)
class UserTrackingPointAdmin(admin.ModelAdmin):
    list_display = ["user_id", "label", "date", "value"]
    list_filter = ["user_id", "label", "date"]
    search_fields = ["user_id", "label"]


@admin.register(UserTrackingLabel)
class UserTrackingLabelAdmin(admin.ModelAdmin):
    list_display = ["label", "description"]
    list_filter = ["label"]
    search_fields = ["label", "description"]
