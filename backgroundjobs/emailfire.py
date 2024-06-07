import time,requests,json,os
from datetime import datetime, timedelta
from Orders.models import Order
from django.db.models import Count, Sum, Max, Avg, Case, When, Value, IntegerField, BooleanField
from django.db.models.functions import ExtractYear, ExtractMonth,ExtractWeek, ExtractWeekDay
from django.db.models.functions import Extract
from backgroundjobs.models import backgroundjobs
from Brands.models import Company
from Outlet.models import OutletProfile
from Product.models import Product, Product_availability
from django.db import connections
from Customers.models import CustomerProfile
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from zapio.settings import Media_Path
from django.db.models import Q
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from UserRole.models import *
from Configuration.models import *

def addr_set():
	domain_name = "https://zapio-admin.com/media/"
	return domain_name


def email_send_module(finaldata,company_id,end_date1,start_date1):
	try:
		cdata = Company.objects.filter(id=company_id)[0]
		now   = datetime.now()
		time  = now.strftime("%d/%b/%y %I:%M %p")
		query = Order.objects.filter(Q(order_time__lte=end_date1),Q(order_time__gte=start_date1),\
					Q(Company_id=company_id),Q(order_status=6))
		if query.count() > 0:
			sub_result = query.values('Company').\
									annotate(total_revenue=Sum('total_bill_value'),order_count=Count("id"))
			alltotal        = round(sub_result[0]['total_revenue'],2)
			totalordercount = sub_result[0]['order_count']
			average_order   = sub_result[0]['total_revenue'] // sub_result[0]['order_count']
		else:
			alltotal = 0
			totalordercount = 0
			average_order = 0
		
		nm = Order.objects.filter(Q(order_time__month=now.month),Q(Company_id=company_id))
		if nm.count() > 0:
			sb_result = nm.values('Company').\
									annotate(total_revenue=Sum('total_bill_value'),order_count=Count("id"))
			totalmtd = round(sb_result[0]['total_revenue'],2)
			totalmtd_count = sb_result[0]['order_count']
		else:
			totalmtd = 0
			totalmtd_count = 0
		url = "https://api.sendgrid.com/v3/mail/send"
		headers = {'Content-type': 'application/json',
			"Authorization": "Bearer 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 ",
		   'Accept': 'application/json'}
		data = {
			  "personalizations": [
				{
				  "to": [
					{
					  "email": cdata.company_email_id,
					},

				  ],
				  "dynamic_template_data": {
				  "items1":finaldata,
				  "Company":cdata.company_name,
				  "time":time,
				  "alltotal": alltotal,
				  "totalordercount" : totalordercount,
				  "average_order"  : average_order,
				  "totalmtd"  :totalmtd,
				  "totalmtd_count" : totalmtd_count
				  },

				}
			  ],
			  "from": {
				"email": "tech@eoraa.com",
				"name" : cdata.company_name
			  },
				"subject": "Hello, World!",
				"template_id":"d-948b70e13b664d63ae43f5d59ff8893b",
				"content": [{"type": "text/html", "value": "Heya!"}]
			}
		response= requests.post(url,data=json.dumps(data),headers=headers)
		print(response)
	except Exception as e:
		print(e)




def daysaleEmail():
	print("Daily Sales Report.....................")
	from datetime import datetime
	now = datetime.now()
	current_time = now.strftime("%I:%M:%S:%p")
	now = datetime.now()
	month = now.month
	yesterday = str(now - timedelta(days=1))
	fy = yesterday.split(' ')
	start_date = fy[0] + str(' 10:00:00.000000')
	end_date = fy[0] + str(' 23:59:59.000000')
	# Same Day today
	# fnow = str(now)
	# fy = fnow.split(' ')
	# start_date1 = fy[0] + str(' 01:00:00.000000')
	# end_date1 = fy[0] + str(' 04:00:00.000000')
	# brand = Company.objects.filter(active_status=1)
	fnow = str(now)
	fy = fnow.split(' ')
	start_date1 = fy[0] + str(' 08:00:00.000000')
	end_date1 = fy[0] + str(' 23:59:59.000000')
	brand = Company.objects.filter(active_status=1)
	k = 1
	finaldata = []
	ordata = []
	ordata1 = []
	fdata = []
	mtime = '11:59:00:PM'
	flag = 0
	if current_time == mtime:
		print("b")
		allbrand = Company.objects.filter(active_status=1)
		for i in allbrand:
			finaldata = []

			alloutlet = OutletProfile.objects.filter(Q(Company_id= i),Q(is_hide=0))
			if alloutlet.count() > 0:
				for index in alloutlet:
					ord_dict = {}
					
					query = Order.objects.filter(Q(order_time__lte=end_date1),Q(order_time__gte=start_date1),\
						Q(outlet_id=index.id),Q(order_status=6))
					
					nm = Order.objects.filter(Q(order_time__month=now.month),Q(outlet_id=index.id),Q(order_status=6))
					if nm.count() > 0:
						sb_result = nm.values('Company').\
										annotate(total_revenue=Sum('total_bill_value'),order_count=Count("id"))
						ord_dict['mtd'] = round(sb_result[0]['total_revenue'],2)
					else:
						ord_dict['mtd'] = 0
					ord_dict['Company'] = Company.objects.filter(id=i.id)[0].company_name
					
					if query.count() > 0:
						sub_source = query.values('order_source').\
										annotate(total_revenue=Sum('total_bill_value'),order_count=Count("id"))
						source_data = []
						for s in sub_source:
							oc = {}
							s_data = s['order_source']
							oc['source'] = OrderSource.objects.filter(id=s['order_source'])[0].source_name
							oc['source_count'] = s['order_count']
							oc['source_value'] = round(s['total_revenue'],2)
							source_data.append(oc)
						ord_dict['final_source'] = source_data
					else:
						pass
					if query.count() > 0:
						sub_result = query.values('Company').\
										annotate(total_revenue=Sum('total_bill_value'),order_count=Count("id"))
						ord_dict['outlet'] = index.Outletname
						ord_dict['total'] = round(sub_result[0]['total_revenue'],2)
						ord_dict['order_count'] = sub_result[0]['order_count']
						ord_dict['ttime'] = now.strftime("%d/%b/%y %I:%M %p")
						ord_dict['average_order'] = sub_result[0]['total_revenue'] // sub_result[0]['order_count']
						finaldata.append(ord_dict)
					else:
						pass
						# ord_dict['outlet'] = index.Outletname
						# ord_dict['total'] = 0
						# ord_dict['order_count'] = 0
						# ord_dict['ttime'] = now.strftime("%d-%b-%y %I:%M %p")
						# ord_dict['average_order'] = 0
						# finaldata.append(ord_dict)
				email_send_status = email_send_module(finaldata,i.id,end_date1,start_date1)
			else:
				pass



def UpdateRider():
	from datetime import datetime
	now = datetime.now()
	current_time = now.strftime("%I:%M:%S:%p")
	mtime = '07:00:00:AM'
	if current_time == mtime:
		alld = ManagerProfile.objects.filter(is_rider=1)
		if alld.count() > 0:
			for index in alld:
				rider_data = ManagerProfile.objects.filter(id=index.id)
				rider_data.update(is_assign=0)
		else:
			pass



