from django.urls import path
from Notification.Api.brand.notification import (orderNotificationCount,
													orderNotificationAll,
													orderNotificationSeen,
													)

from Notification.Api.outlet.order_notification import (orderNotificationCount,
													orderNotificationAll,
													orderNotificationSeen,
													)
from .views import *

urlpatterns = [
	path('outlet/ordernotification/count/',orderNotificationCount.as_view()),
	path('outlet/ordernotification/all/',orderNotificationAll.as_view()),
	path('outlet/ordernotification/seen/',orderNotificationSeen.as_view()),

	path('brand/ordernotification/count/',orderNotificationCount.as_view()),
	path('brand/ordernotification/all/',orderNotificationAll.as_view()),
	path('brand/ordernotification/seen/',orderNotificationSeen.as_view()),
	path('list/',NotificationList.as_view()),
	path('eventlist/',EventList.as_view()),


]