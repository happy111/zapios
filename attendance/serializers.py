from rest_framework import serializers
from .models import StaffAttendance,AttendanceTime
from UserRole.models import ManagerProfile, UserType
from datetime import datetime

class AttendanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffAttendance
        fields = "__all__"

class AttendanceTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceTime
        fields = "__all__"

class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = ("user_type",)


class FilteredListSerializer(serializers.ListSerializer):
    """Serializer to filter the active system, which is a boolen field in
       System Model. The value argument to to_representation() method is
      the model instance"""
    def to_representation(self, data):
        data = data.filter(created_at__date=datetime.now().date())
        return super(FilteredListSerializer, self).to_representation(data)

class AttendanceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffAttendance
        list_serializer_class = FilteredListSerializer
        fields = "__all__"

class AttendanceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffAttendance
        fields = ("is_billprint", "temperature")


class ManagerProfileSerializer(serializers.ModelSerializer):
   # staff_attendance = AttendanceListSerializer(read_only=True, many=True)
  user_type = UserTypeSerializer(read_only=True)
  staff_attendance = serializers.SerializerMethodField()
  class Meta:
      model = ManagerProfile
      fields = ("id","manager_name","last_name","user_type","Company", "staff_attendance")



  def get_staff_attendance(self, obj):
      sdata = StaffAttendance.objects.filter(profile_id=obj.id,created_at__date=datetime.now().date())
      finaldata = []
      if sdata.count() > 0:
          atdance_time = AttendanceTime.objects.filter(attendance_id=sdata[0].id)
          if atdance_time.count() > 0:
              for index in atdance_time:
                  dic = {}
                  dic['id'] = index.id
                  dic['time_in']= index.time_in
                  dic['time_out'] = index.time_out
                  dic['created_at'] = index.created_at
                  dic['status'] = index.status
                  dic['is_billprint'] = sdata[0].is_billprint
                  dic['temperature'] = sdata[0].temperature
                  dic['profile'] = sdata[0].profile_id
                  finaldata.append(dic)
          else:
              pass
      else:
          pass
      return finaldata