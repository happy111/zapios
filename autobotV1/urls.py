"""zapio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from autobotV1 import settings

urlpatterns = [
]

import time, threading
# from backgroundjobs.jobs import brand_report, outlet_report
from backgroundjobs.notify_sound import soundeffect
from django.db import connections
from backgroundjobs.order_mapper import items_description, delete_orders, delete_one
from backgroundjobs.emailfire import daysaleEmail,UpdateRider
from backgroundjobs.basic_config import BasicSetting


# WAIT_SECONDS = 1
# def update_emailprocessing():
# 	sale_report_generation = daysaleEmail()
# 	threading.Timer(WAIT_SECONDS, update_emailprocessing).start()
# update_emailprocessing()

# WAIT_SECONDS = 1
# def update_rider():
# 	rider_report_generation = UpdateRider()
# 	threading.Timer(WAIT_SECONDS, update_rider).start()
# update_rider()


# WAIT_SECONDS = 1
# def update_brand_basic_configuration():
# 	basic_setting = BasicSetting()
# 	threading.Timer(WAIT_SECONDS, update_brand_basic_configuration).start()
# update_brand_basic_configuration()


