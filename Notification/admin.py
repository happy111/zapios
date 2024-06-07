from django.contrib import admin
from Notification.models import NotificationConfiguration, NotificationRecord,NotificationCard
from datetime import datetime

# from cashyfood.admin_validation import NotificationConfigurationForm
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter


def make_active(modeladmin, request, queryset):
    queryset.update(active_status="1")


make_active.short_description = "Move Items to Active"


def make_deactive(modeladmin, request, queryset):
    queryset.update(active_status="0")


make_deactive.short_description = "Move Items to Inactive"


# class NotificationConfigurationAdmin(admin.ModelAdmin):
#     # form = NotificationConfigurationForm
#     exclude = ["active_status", "created_at", "updated_at", "created_by", "updated_by"]
#     list_filter = [
#         "active_status",
#         "notification_for",
#         ("created_at", DateRangeFilter),
#         ("updated_at", DateRangeFilter),
#         "created_by",
#         "updated_by",
#     ]
#     search_fields = ["notification_type", "description"]

#     list_display = [
#         "notification_type",
#         "description",
#         "notification_for",
#         "active_status",
#         "created_at",
#         "updated_at",
#         "created_by",
#         "updated_by",
#     ]

#     actions = [make_active, make_deactive]

#     list_per_page = 10

#     def has_delete_permission(self, request, obj=None):
#         return False

#     def save_model(self, request, obj, form, change):
#         if not change:
#             obj.created_by = request.user
#         else:
#             obj.updated_by = request.user
#             obj.updated_at = datetime.now()
#         obj.save()


# class NotificationRecordAdmin(admin.ModelAdmin):
#     exclude = ["notification_category", "notification_for", "updated_by"]

#     list_filter = [
#         "notification_category",
#         "status",
#         "reason_for_failed",
#         "notification_for",
#         ("created_at", DateRangeFilter),
#     ]

#     search_fields = ["user__username", "user__email", "user__mobile", "massge_body"]

#     list_display = [
#         "notification_category",
#         "notification_type",
#         "status",
#         "notification_for",
# #        "user_admin",
#         "massge_body",
#         "reason_for_failed",
#         "created_at",
#     ]

#     list_per_page = 10

#     readonly_fields = [
#         "notification_category",
#         "notification_type",
#         "user",
#         "notification_for",
#         "otp",
#         "status",
#         "is_read",
#         "reason_for_failed",
#         "message_data",
#         "massge_body",
#     ]

#     def has_add_permission(self, request, obj=None):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False

#     def save_model(self, request, obj, form, change):
#         if not change:
#             obj.created_by = request.user
#         else:
#             obj.updated_by = request.user
#             obj.updated_at = datetime.now()
#         obj.save()


# admin.site.register(NotificationConfiguration, NotificationConfigurationAdmin)
# admin.site.register(NotificationRecord, NotificationRecordAdmin)

class NotificationCardAdmin(admin.ModelAdmin):

    list_display = [
        "subject",
        "content",
        "status",
    ]

    exclude = ["active_status", "created_at", "updated_at","outlet"]


    def has_add_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
            obj.updated_at = datetime.now()
        obj.save()

admin.site.register(NotificationCard, NotificationCardAdmin)


