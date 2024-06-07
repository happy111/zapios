from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from UserRole.models import ManagerProfile
from attendance.models import StaffAttendance,AttendanceTime
from .serializers import (NotificationSerializer)
from datetime import datetime
from rest_framework import status
from django.http import Http404
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_406_NOT_ACCEPTABLE,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_204_NO_CONTENT,
)
from Notification.models import *



class NotificationList(ListAPIView):
    """
    Notification Listing GET API

        Service Usage and Description : This Api is used to provide Notification.
        Authentication Required : YES

        Params : {
            "status"  :   True
        }

        Response : {
            "data" : final_data
        }
    """

    permission_classes = (IsAuthenticated,)
    serializer_class   = NotificationSerializer
    def get_queryset(self,format=None):
        queryset = NotificationCard.objects.filter(active_status=1).order_by('-created_at')
        return queryset
    def get(self, request):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            final_data = []
            if queryset.count() > 0:
                for index in queryset:
                    q_dict = {}
                    q_dict["id"]            = index.id
                    q_dict["subject"]       = index.subject 
                    q_dict["active_status"] = index.active_status
                    q_dict["content"]       = index.content
                    q_dict["created_at"]       = index.created_at.isoformat()
                    final_data.append(q_dict)
            return Response(final_data, status=HTTP_200_OK)
        except Exception as e:
            return Response(
                {"success": False, "message": str(e)}, status=HTTP_406_NOT_ACCEPTABLE
            )




class EventList(ListAPIView):
    """
    Event Listing GET API

        Service Usage and Description : This Api is used to provide event.
        Authentication Required : YES

        Params : {
            "status"  :   True
        }

        Response : {
            "data" : final_data
        }
    """

    permission_classes = (IsAuthenticated,)
    serializer_class   = NotificationSerializer
    def get_queryset(self,format=None):
        queryset = NotificationCard.objects.filter(active_status=1).order_by('-created_at')
        return queryset
    def get(self, request):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            final_data = []
            if queryset.count() > 0:
                for index in queryset:
                    q_dict = {}
                    q_dict["id"]            = index.id
                    q_dict["subject"]       = index.subject 
                    q_dict["active_status"] = index.active_status
                    q_dict["content"]       = index.content
                    q_dict["created_at"]       = index.created_at.isoformat()
                    final_data.append(q_dict)
            return Response(final_data, status=HTTP_200_OK)
        except Exception as e:
            return Response(
                {"success": False, "message": str(e)}, status=HTTP_406_NOT_ACCEPTABLE
            )