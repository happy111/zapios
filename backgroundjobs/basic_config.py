import time
import requests
import json
import os


from datetime import datetime, timedelta
from django.db.models import Count, Sum, Max, Avg, Case, When, Value, IntegerField, BooleanField
from Brands.models import Company
from Outlet.models import *

from django.db import connections
from django.db.models import Q
from Notification.models import NotificationCard
from Configuration.models import *





# def BasicSetting():
# 	from datetime import datetime
# 	now = datetime.now()
# 	current_time = now.strftime("%I:%M:%S:%p")
# 	mtime = '07:00:00:AM'
# 	allbrand = Company.objects.filter(active_status=1)
# 	flag = 0
# 	for index in allbrand:
# 		outlet_data = OutletProfile.objects.filter(Company_id=index.id)
# 		if outlet_data.count() > 0:
# 			for temp in outlet_data:
# 				if temp.Outletname != None and temp.address != None:
# 					timdata = OutletTimingMaster.objects.filter(outlet_id=temp.id)
# 					if timdata.count() > 0:
# 						if temp.delivery_zone != None and len(temp.delivery_zone) > 0:
# 							flag = 1
# 				if flag == 1:
# 					notification_data = NotificationCard.objects.filter(subject='Outlet')
# 					if notification_data.count() > 0:
# 						outlet_data = notification_data[0].outlet
# 						if outlet_data != None:
# 							if str(index.id) in outlet_data:
# 								pass
# 							else:
# 								outlet_data.append(index.id)
# 								notification_data.update(outlet=outlet_data)
# 						else:
# 							outlet = []
# 							outlet.append(index.id)
# 							notification_data.update(outlet=outlet)
# 		else:
# 			pass
# 		flag = 0



def BasicSetting():
	try:
		import csv
		with open('/home/umesh/Downloads/PINCODE - Version2.csv', 'r') as file:
			reader = csv.reader(file)
			for row in reader:
				pd = {}
				obj_data = Address.objects.filter(pincode=row[0])
				if obj_data.count() > 0:
					print(row[0])
				else:
					pd['pincode'] = row[0]
					pd['prefecture'] = row[1]
					pd['city'] = row[2]
					pd['address'] = row[3]
					getLoc = Address.objects.create(pincode=pd['pincode'],prefecture=pd['prefecture'] ,city=row[2],address=row[3])
					getLoc.save()
	except Exception as e:
		print(e)












