from Product.models import *
import re
from django.conf import settings
from ZapioApi.api_packages import *
from datetime import datetime
from django.db.models import Q
import datetime
from discount.models import Coupon



def check_coupon(data,ccode,company):
	actual_response = {}
	product_data = data['cart']
	Old_subtotal  = 0
	tdaprice = 0
	coupon_applied = 0
	today = datetime.datetime.now()
	discount_price = 0
	query = Coupon.objects.filter(coupon_code__exact=ccode,frequency__gte=1,
							valid_till__gte=today,Company=company)

	if query.count()!=0:
		is_min_shoppping = query[0].is_min_shop
		total_product_price = 0
		for i in range(len(product_data)):
			pname = product_data[i]['name']
			pprice = product_data[i]['price'] # old price
			pid = str(product_data[i]['product_id'])
			quantity = product_data[i]['quantity']
			nprice = float(pprice) * int(quantity)
			coupon_checking,flag = coupon_integrity(query,company,pid)
			

			q = query[0]
			Old_subtotal = float(Old_subtotal) + float(nprice)

			if len(coupon_checking) != 0 and flag == 1:
				total_product_price = float(total_product_price) + float(nprice)

			if len(coupon_checking) != 0 and flag == 2:
				if pid in coupon_checking:
					total_product_price = float(total_product_price) + nprice

			if len(coupon_checking) == 0 and flag == 0:
				total_product_price = float(total_product_price) + float(nprice)

		if is_min_shoppping == True:
			if query[0].min_shoping <= total_product_price and query[0].max_shoping >= total_product_price:
				coupon_applied=1
				if q.coupon_type == "Flat":
					discount_price = query[0].flat_discount
					act_discount = float(total_product_price) - float(query[0].flat_discount)
				else:
					discount_price = float(total_product_price) * float(query[0].flat_percentage)/100
					act_discount = float(total_product_price) - float(discount_price)
			else:
				coupon_applied=0

		else:
			print("XX")
			coupon_applied=1

			if q.coupon_type == "Flat":
				print("VV")
				discount_price = query[0].flat_discount
				act_discount = float(total_product_price) - float(query[0].flat_discount)
			else:
				print("CC",total_product_price)
				discount_price = float(total_product_price) * float(query[0].flat_percentage)/100
				act_discount = float(total_product_price) - float(discount_price)
				print("aa",discount_price)
	actual_response["Old_subtotal"]  = Old_subtotal
	actual_response["coupon_applied"] = coupon_applied
	actual_response["tdaprice"] = discount_price
	


	return actual_response



def coupon_integrity(query,company,pid):
	flag = 0
	if query.count() > 0:
		q = query[0]
		mapped_products = q.product_map
		if mapped_products==None or mapped_products=="" or len(mapped_products) == 0:
			mapped_cat = q.category_id
			if mapped_cat != None:
				flag = 1
				products = Product.objects.filter(id=pid,product_categorys__exact=[str(mapped_cat)],\
					active_status=1,Company_id = company)
				p_ids = []
				if products.count() != 0:
					for i in products:
						p_ids.append(str(i.id))
				else:
					pass
				mapped_products = p_ids
			else:
				mapped_products = []
		else:
			flag = 2
			p_ids = []
			for j in mapped_products:
				products = Product.objects.filter(id=j,active_status=1,Company_id = company)
				if products.count() != 0 :
					p_ids.append(str(j))
				else:
					pass
			mapped_products = p_ids
	else:
		flag = 3
		mapped_products = []
	return mapped_products,flag


def calculate_tax(Old_subtotal,tdaprice,data):
	old_tax = data['tax']
	percent = float(old_tax) / float(Old_subtotal)
	tax_percent = percent * 100
	avalue = float(Old_subtotal) - float(tdaprice)
	tvalue = round(float(avalue) * tax_percent / 100,2)
	return tvalue
