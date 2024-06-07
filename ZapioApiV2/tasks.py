from __future__ import unicode_literals, absolute_import
from celery.schedules import crontab
from celery.task import periodic_task
from zapio.celery import app
from celery import shared_task
from Brands.models import Company
from Subscription.models import SubscriptionPlanType
import requests, json

from datetime import datetime, timedelta
from Orders.models import Order
from django.db.models import Count, Sum, Max, Avg, Case, When, Value, IntegerField, BooleanField
from django.db.models.functions import ExtractYear, ExtractMonth,ExtractWeek, ExtractWeekDay
from django.db.models.functions import Extract
from backgroundjobs.models import backgroundjobs,Eventjobs
from Brands.models import Company
from Outlet.models import OutletProfile
from Product.models import Product, Product_availability
from django.db import connections
from Customers.models import CustomerProfile
from ZapioApi.api_packages import *
from Configuration.models import PaymentMethod,WebsiteStatistic,OrderSource
from Event.models import HistoryEvent

@shared_task
def print_hello():
    print('Hello World!')
    for company in Company.objects.filter(active_status=1, company_name="umesh"):
        print("company",company)
        subscription = SubscriptionPlanType.objects.filter(id=company.plan_name_id, active_status=1).first()
        if subscription:
            data = {}
            data["amount"] = str(subscription.cost)
            customer = {}
            customer["name"] = str(company.company_name)
            data["description"] = "Payment for the subscription plan "  + str(subscription.plan_name)
            customer["email"] = str(company.company_email_id)
            customer["mobile"] =  str(company.company_contact_no)
            data["customer"] = customer
            data["currency"] = str(company.billing_currency.currency)
            url = "https://zapio-admin.com/" + "api/v2/payment/subscription/"  #"put the subscription payment API url"
            headers = {'Authorization': 'TOKEN d144042ee1005eb1a9331d5656b842394a23938c', 'Content-Type':'application/json'}
            data = json.dumps(data)
            print("data",data)
            response = requests.post(url,data=data, headers=headers)
            print(response.content)
        else:
            print("no Active subscription for ", company.company_name)


@shared_task
def brand_report1():
    return "umesh samal"

@shared_task
def brand_report():
    brand = Company.objects.filter(active_status=1)
    for b in brand:
        order_record = Order.objects.filter(Company_id=b.id)
        if order_record.count() == 0:
            pass
        else:
            company_id = order_record[0].Company_id
            now = datetime.now()
            year = now.year
            month = now.month
            today = now.day
            todate = now.date()
            order_result = order_record.values('Company').\
                            annotate(total_revenue=Sum('total_bill_value'),order_count=Count("id"))
            c = order_record.filter(order_time__year=year,\
                order_time__month=month,order_time__day=today)
            order_today = c.count()
            if order_today > 0:
                tevenue = c.values('Company').\
                            annotate(total_revenue=Sum('total_bill_value'),order_count=Count("id"))
                today_revenue = tevenue[0]["total_revenue"]

                tax_result = c.values('Company').\
                            annotate(total_tax=Sum('taxes'),order_count=Count("id"))
                dis_result = c.values('Company').\
                            annotate(total_discount=Sum('discount_value'),order_count=Count("id"))
                today_tax = tax_result[0]['total_tax']
                today_discount = dis_result[0]['total_discount']
            else:
                today_revenue = 0
                today_tax = 0
                today_discount = 0
            completed_orders = order_record.filter(is_completed=1).count()
            pending_orders = order_record.filter(is_completed=0).count()
            final_result = []
            card_dict = {}
            #  Today Order Details
            card_dict["today_order_count"] = order_today
            card_dict["today_order_sale"] = today_revenue
            card_dict["today_total_tax"] = today_tax
            card_dict["today_total_discount"] = today_discount
            card_dict["no_menu_views"] = 0
            card_dict["no_user_reach_checkout"] = 0

            ws = WebsiteStatistic.objects.filter(company_id=company_id)
            c = ws.filter(created_at__year=year,\
                created_at__month=month,created_at__day=today,visitors=1)
            if c.count() > 0:
                card_dict["no_visitiors"] = c.count()
            else:
                card_dict["no_visitiors"] = 0
            m = ws.filter(created_at__year=year,\
                created_at__month=month,created_at__day=today,menu_views=1)
            if m.count() > 0:
                card_dict["no_menu_views"] = m.count()
            else:
                card_dict["no_menu_views"] = 0
            source_data = OrderSource.objects.filter(source_name='Website Order',company_id=company_id)
            if source_data.count() > 0:
                online_order = order_record.filter(order_time__year=year,\
                order_time__month=month,order_time__day=today,order_source_id=source_data[0].id)
                if online_order.count() > 0:
                    card_dict["no_online_orders"] = online_order.count()
                else:
                    card_dict["no_online_orders"] = 0
            else:
                card_dict["no_online_orders"] = 0
            #For best seller report ends here!!
           
            #For best seller report
            best_seller = order_record.all()
            all_orders = []
            best_list_id = []
            id_wise_freq = {}
            id_wise_price = {}
            for i in best_seller:
                orders = i.order_description
                for o in orders:
                    all_orders.append(o)

            for j in all_orders:
                if 'id' in j:
                    best_list_id.append(j["id"])
                    id_wise_price[j["id"]] = int(j["price"])
                else:
                    pass
                if 'product_id' in j:
                    best_list_id.append(j["product_id"])

                    id_wise_price[j["product_id"]] = int(j["price"])

            for k in best_list_id:
                id_wise_freq[k] = best_list_id.count(k)
            best_seller_map = \
            {k : v * id_wise_price[k] for k, v in id_wise_freq.items() if k in id_wise_price}
            l1 = []
            l2 = []
            l3 = []
            final_best_seller_ids = []
            for l in best_seller_map.values():
                l1.append(l)
            l1.sort(reverse = True)
            for m,n in best_seller_map.items():
                for  o in l1:
                    if n == o:
                        final_best_seller_ids.append(m)
                    else:
                        pass
            card_dict["best_seller"] = []
            for p in final_best_seller_ids:
                product_q = Product.objects.filter(id=p)
                if product_q.count() != 0:
                    product_dict = {}
                    product_dict["id"] = p
                    product_dict["product_name"] = product_q[0].product_name
                    product_dict["food_type"] = product_q[0].food_type.food_type
                    product_dict["product_desc"] = product_q[0].product_desc
                    card_dict["best_seller"].append(product_dict)
                else:
                    pass
            card_dict["order_details"] = []
            today_order = order_record.filter(order_time__date=todate).order_by('-order_time')
            for l in today_order:
                order_dict = {}
                order_dict['id'] = l.id
                order_dict['order_id'] = l.order_id
                order_dict['order_status'] = l.order_status.Order_staus_name
                order_dict['total_bill_value'] = l.total_bill_value
                order_dict['total_items'] = l.total_items
                o_time = l.order_time + +timedelta(hours=5,minutes=30)
                order_dict['order_time'] = o_time.strftime("%d/%b/%y %I:%M %p")
                if l.delivery_time != None:
                    d = l.delivery_time+timedelta(hours=5,minutes=30)
                    order_dict["delivery_time"] = d.strftime("%d/%b/%Y %I:%M %p")
                else:
                    order_dict['delivery_time'] = None
                if l.settlement_details !=None:
                    if len(l.settlement_details) > 0: 
                        order_dict['payment_mode'] = l.settlement_details[0]['payment_name']
                order_dict['outlet_name'] = l.outlet.Outletname
                order_dict['is_paid'] = l.is_paid
                order_dict["can_process"] = True
                if l.order_status.can_process == 1:
                    pass
                else:
                    order_dict["can_process"] = False
                card_dict["order_details"].append(order_dict)

            cp = order_record.filter(order_time__year=year,\
                order_time__month=month,order_time__day=today)
            Outletwise_revenue = \
                cp.values('Company','outlet__Outletname').\
                        annotate(revenue=Sum('total_bill_value'),order_count=Count("id"))\
                        .order_by('-revenue')
            card_dict["outlet_revenue"] = []
            if Outletwise_revenue.count() != 0:
                for j in Outletwise_revenue:
                    revenue_dict = {}
                    revenue_dict["outlet_name"] = j["outlet__Outletname"]
                    revenue_dict["revenue"] = j["revenue"]
                    revenue_dict["order_count"] = j["order_count"]
                    card_dict["outlet_revenue"].append(revenue_dict)
            else:
                pass
            final_result.append(card_dict)
            data_check = backgroundjobs.objects.filter(Company_id=company_id)
            if data_check.count() == 0:
                data_create = backgroundjobs.objects.create(Company_id=company_id,report=final_result)
            else:
                data_check.update(report=final_result,updated_at=now)
    close_all = connections.close_all()
    return "I have updated report successfully!!"



