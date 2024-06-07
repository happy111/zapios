from rest_framework import serializers

from Notification.models import NotificationRecord


class NotificationSerializer(serializers.ModelSerializer):
	class Meta:
		model = NotificationRecord
		exclude = ('admin_user',
				   'user',
				   'notification_type',
				   'is_read',
				   'otp',
				   'reason_for_failed',
				   'notification_for',
				   'status') 


class NotificationRecordSerializer(serializers.ModelSerializer):
	class Meta:
		model = NotificationRecord
		fields = '__all__' 
