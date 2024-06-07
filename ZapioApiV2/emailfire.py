from __future__ import unicode_literals, absolute_import
from celery.schedules import crontab
from celery.task import periodic_task
from zapio.celery import app
from celery import shared_task
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
from zapio.settings import EMAIL_HOST_USER, Media_Path
from django.db.models import Q
import time


def addr_set():
	domain_name = "https://zapio-admin.com/media/"
	return domain_name

def email_send_module(toe,send_data,d):
	try:
		subject = "Today Order Summary"
		from_email = EMAIL_HOST_USER
		to = toe
		cc_email_id = []

		to_email =[to]
		# to_email =[to,order_mail]
		html_content = render_to_string('email_templates/sale-emailer.html',{"data":send_data,"data1":d})
		text_content = strip_tags(html_content)
		msg = EmailMultiAlternatives(subject, text_content, from_email, to_email, cc=cc_email_id)
		msg.attach_alternative(html_content, "text/html")
		result_of_mail = msg.send()
		return result_of_mail
	except Exception as e:
		print(e)




@shared_task
def daysaleEmail():
	print("ssssssssssssssssssss")
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
	mtime = '11:45:00:PM'
	flag = 0
	
	if current_time == mtime:
		alloutlet = OutletProfile.objects.filter(Company_id= 13)
		for index in alloutlet:
			ord_dict = {}
			query = Order.objects.filter(Q(order_time__lte=end_date1),Q(order_time__gte=start_date1),\
				Q(outlet_id=index.id))
			nm = Order.objects.filter(Q(order_time__month=now.month),Q(outlet_id=index.id))
			if nm.count() > 0:
				sb_result = nm.values('Company').\
								annotate(total_revenue=Sum('total_bill_value'),order_count=Count("id"))
				ord_dict['mtd'] = sb_result[0]['total_revenue']
			else:
				ord_dict['mtd'] = 0
			ord_dict['Company'] = Company.objects.filter(id=13)[0].company_name
			if query.count() > 0:
				sub_result = query.values('Company').\
								annotate(total_revenue=Sum('total_bill_value'),order_count=Count("id"))
				ord_dict['outlet'] = index.Outletname
				ord_dict['total'] = sub_result[0]['total_revenue']
				ord_dict['order_count'] = sub_result[0]['order_count']
				ord_dict['ttime'] = now.strftime("%d/%b/%y %I:%M %p")
				ord_dict['average_order'] = sub_result[0]['total_revenue'] // sub_result[0]['order_count']
				finaldata.append(ord_dict)
			else:
				ord_dict['outlet'] = index.Outletname
				ord_dict['total'] = 0
				ord_dict['order_count'] = 0
				ord_dict['ttime'] = now.strftime("%d-%b-%y %I:%M %p")
				ord_dict['average_order'] = 0
				finaldata.append(ord_dict)
		#to_emailID = 'rahul.p@thegrammarroom.com'
		to_emailID = 'umeshsamal3@gmail.com'
		email_send_status = email_send_module(to_emailID,finaldata,ord_dict)
		return email_send_status





