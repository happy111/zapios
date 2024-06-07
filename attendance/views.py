from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from UserRole.models import ManagerProfile
from attendance.models import StaffAttendance,AttendanceTime
from attendance.serializers import (AttendanceCreateSerializer, 
                                    ManagerProfileSerializer, 
                                    AttendanceUpdateSerializer,
                                    AttendanceTimeSerializer)
from datetime import datetime
from rest_framework import status
from django.http import Http404
from django.db import transaction
from django.http import Http404
from django.utils.translation import gettext_lazy

class AttendanceCreate(CreateAPIView):
    """
    Add Attendance Post API, This API can be used to login(via present status) or to mark absent(any of 4 type of leave)

        Authentication Required		 	: 		Yes
        Service Usage & Description	 	: 		This Api is used to add attandance for staff.

        Data Post: {

            "staff_id"         : "23", //required
            "temperature"      : "97",
            'is_billprint'     : "true",
            "status"           : "present/weakoff/lwp/cl/el" //required
        }

        Response: {
                data = {....},
                status=status 201/400/423/404
        }

    """

    permission_classes = (IsAuthenticated,)
    serializer_class = AttendanceCreateSerializer
    queryset = StaffAttendance.objects.all()

    def post(self, request, *args, **kwargs):
        data = self.request.data
        time_data = {}
        staff = ManagerProfile.objects.filter(id=data["staff_id"])
        if not staff:
            return Response(status=status.HTTP_404_NOT_FOUND)
        attendance = StaffAttendance.objects.filter(
            profile_id=data["staff_id"], created_at__date=datetime.now().date()
        )
        if attendance:
            if attendance[0].active_status == True:
                return Response(status=status.HTTP_423_LOCKED)
            if data['status'] == 'present':
                time_data["time_in"] = datetime.now()
                time_data["active_status"] = 1
            time_data['attendance_id'] = attendance[0].id
            time_data["status"] = data['status']
            serializers = AttendanceTimeSerializer(data=time_data)
            if serializers.is_valid(raise_exception=True):
                serializers.save()
                attendance.update(active_status=1)
                queryset = AttendanceTime.objects.filter(created_at__date=datetime.now().date(),attendance_id=attendance[0].id)
                serializer = AttendanceTimeSerializer(queryset, many=True)
                return Response(data=serializers.data, status=status.HTTP_201_CREATED)

        data["auth_user"] = self.request.user.id
        data["profile"] = data["staff_id"]
        if data["status"] == "present":
            data["active_status"] = 1
            data["time_in"] = datetime.now()
        serializer = AttendanceCreateSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            if data['status'] == 'present':
                time_data["time_in"] = datetime.now()
            time_data['attendance_id'] = serializer.data['id']
            time_data["status"] = data['status']
            serializers = AttendanceTimeSerializer(data=time_data)
            if serializers.is_valid(raise_exception=True):
                serializers.save()
      
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class AttendanceLogout(UpdateAPIView):
    """
    Staff Attendance Logout Update API

        Authentication Required		 	: 		Yes
        Service Usage & Description	 	: 		This Api is used to add attandance for staff.

        Request body
        {
            "staff_id":1  //required
        }

    """

    permission_classes = (IsAuthenticated,)
    serializer_class = AttendanceCreateSerializer
    queryset = StaffAttendance.objects.all()

    def get_object(self):
        try:
            data = self.request.data
            obj = StaffAttendance.objects.get(
                profile_id=data["staff_id"],
                created_at__date=datetime.now().date(),
                status="present",
                active_status=1
            )
            obj.active_status=0
            obj.time_out=datetime.now()
            obj.save()
            st = AttendanceTime.objects.filter(attendance_id_id=obj.id).last()
            st.active_status=0
            st.time_out=datetime.now()
            st.save()
            return obj
        except Exception as e:
            print(e)
            raise Http404


class AttendanceUpdate(UpdateAPIView):
    """
    Staff Attendance Update API (can be used for temperature and is_billprint)

        Authentication Required		 	: 		Yes
        Service Usage & Description	 	: 		This Api is used to add attandance for staff.

        Request body
        {
            "staff_id":12         //optional
            "temperature":95 ,    //optional
            "is_billprint":1,     //optional
        }
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = AttendanceUpdateSerializer
    queryset = StaffAttendance.objects.all()

    def get_object(self):
        try:
            data = self.request.data
            obj = StaffAttendance.objects.get(
                profile_id=data["staff_id"],
                created_at__date=datetime.now().date(),
                status="present",
                active_status=1
            )
            serializer = AttendanceUpdateSerializer(obj,data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return obj
        except Exception as e:
            print(e)
            raise Http404

class AttendanceList(ListAPIView):
    """
	Attandance data post API

		Authentication Required		 	: 		Yes
		Service Usage & Description	 	: 		This Api is used to provide listing staff all information.

		:param: outlet_id   //required

	"""

    permission_classes = (IsAuthenticated,)
    serializer_class = ManagerProfileSerializer
    queryset = ManagerProfile.objects.all()

    def get_queryset(self):
        data = self.request.query_params
        queryset = []
        queryset = ManagerProfile.objects.filter(
            outlet__icontains=data["outlet_id"],
            is_attandance=1,
            active_status=1,
            is_hide=0
        ).order_by('manager_name')
        
        return queryset