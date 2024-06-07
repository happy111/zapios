from Product.models import Variant,Product,Addons
from Configuration.models import *
import datetime
from discount.models import Coupon

def check_coupon(data,ccode):
	actual_response = {}
	product_data = data['order_description']
	company = data['company_id']
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
			nprice = pprice * quantity
			coupon_checking,flag = coupon_integrity(query,company,pid)
			q = query[0]
			Old_subtotal = Old_subtotal + nprice

			if len(coupon_checking) != 0 and flag == 1:
				total_product_price = total_product_price + nprice

			if len(coupon_checking) != 0 and flag == 2:
				if pid in coupon_checking:
					total_product_price = total_product_price + nprice

			if len(coupon_checking) == 0 and flag == 0:
				total_product_price = total_product_price + nprice
			

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
			coupon_applied=1
			if q.coupon_type == "Flat":
				discount_price = query[0].flat_discount
				act_discount = float(total_product_price) - float(query[0].flat_discount)
			else:
				discount_price = float(total_product_price) * float(query[0].flat_percentage/100)
				act_discount = float(total_product_price) - float(discount_price)

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





def calculate_packagecharge(pro_id,product_price,index):
	p_data = Product.objects.filter(id=pro_id)
	packing_charge = 0
	if p_data.count() > 0:
		price_type = p_data[0].price_type
		if p_data[0].is_tax == True:
			t = p_data[0].package_tax
			if t != None:
				if len(t) > 0:
					tax_sum = 0
					for i in t:
						ta = Tax.objects.filter(id=str(i))
						if ta.count() > 0:
							percentage = ta[0].tax_percent
							tax_sum = tax_sum + float(percentage)
		else:
			pass
		
		if price_type != None and price_type == 'Fixed Price':
			amount = p_data[0].packing_amount
			if p_data[0].is_tax == True:
				tax = float(amount) * float(tax_sum) / 100
				packing_charge = round(tax + amount,2) * index['quantity']
			else:
				packing_charge = amount * index['quantity']
		
		if price_type != None and price_type == 'Percentage Price':
			amount = p_data[0].packing_amount
			famount = float(product_price) * float(amount) / 100
			if p_data[0].is_tax == True:
				tax = float(famount) * float(tax_sum) / 100
				packing_charge = round(famount + tax,2) * index['quantity']
			else:
				packing_charge = famount * index['quantity']

	return packing_charge


def calculate_deliverycharge(delivery_detail,product_price):

	if len(delivery_detail) > 0:
		ddata = delivery_detail[0]
		if len(ddata['tax_detail']) > 0:
			tax_sum = 0
			for index in ddata['tax_detail']:
				tax_sum = tax_sum + index['percentage']
		if ddata['price_type'] == 'Fixed Price':
			charge_amount = ddata['amount']
			if len(ddata['tax_detail']) > 0:
				charge_tax = charge_amount * tax_sum / 100
				delivery_charge = charge_tax + charge_amount
			else:
				delivery_charge =  charge_amount
		else:
			charge_amount = float(product_price) * float(ddata['amount']) / 100
			if len(ddata['tax_detail']) > 0:
				charge_tax = charge_amount * tax_sum / 100
				delivery_charge = charge_tax + charge_amount
			else:
				delivery_charge =  charge_amount
	else:
		delivery_charge = 0
	return delivery_charge


def calculate_tax(pid,qty,total_price):
	p_data = Product.objects.filter(id=pid)
	if p_data.count() > 0:
		tax_data = p_data[0].tax_association
		if tax_data != None and len(tax_data) > 0:
			tax = Tax.objects.filter(id__in=tax_data)
			tax_sum = 0
			for i in tax:
				tax_sum = i.tax_percent + tax_sum
			ftax = total_price * tax_sum / 100
			total_tax = ftax
	return total_tax

def calculste_product_price(index):
	product_price = 0
	pro_id = index['product_id']
	p_data = Product.objects.filter(id=pro_id)
	

	if index['is_customize'] == 1:
		pro_id = index['product_id']
		p_data = Product.objects.filter(id=pro_id)
		if p_data.count() > 0:
			if 'add_ons' in index:
				v_id = index['add_ons']
				addon_price = 0
				for k in v_id:
					if k['addon_id'] =='N/A':
						price = k['price']
						addon_price = addon_price + float(price)
					else:
						price = Addons.objects.filter(id=k['addon_id'])[0].addon_amount
						addon_price = addon_price + float(price)
				if addon_price == 0:
					if p_data[0].variant_deatils != None and p_data[0].price == 0:
						min_price = []
						for i in p_data[0].variant_deatils:
							min_price.append(i['price'])
						product_price =  min(min_price)*index['quantity']
					else:
						product_price =   p_data[0].price * index['quantity']
				else:
					product_price =  p_data[0].price*index['quantity'] + addon_price * index['quantity']
			else:
				if p_data[0].variant_deatils != None and p_data[0].price == 0:
					min_price = []
					for i in p_data[0].variant_deatils:
						min_price.append(i['price'])
					product_price =  min(min_price)*index['quantity']
				else:
					product_price = p_data[0].price * index['quantity']	
	else:
		pro_id = index['product_id']
		p_data = Product.objects.filter(id=pro_id)
		if p_data[0].variant_deatils != None and p_data[0].price == 0:
			min_price = []
			for i in p_data[0].variant_deatils:
				min_price.append(i['price'])
			product_price =  min(min_price)*index['quantity']	
		else:
			pro_id = index['product_id']
			p_data = Product.objects.filter(id=pro_id)
			if p_data.count() > 0:
				product_price = p_data[0].price*index['quantity']
	return product_price


def calculate_tax1(data):
	old_tax = data['taxes']
	return old_tax


def calculate_discount(data,ccode):
	apply_coupon  = check_coupon(data,ccode)
	Old_subtotal  =  apply_coupon["Old_subtotal"]
	coupon_applied = apply_coupon["coupon_applied"]
	tdaprice =       apply_coupon["tdaprice"]
	total_tax = calculate_tax1(data)
	return total_tax,tdaprice




def DataVerify(data):
	order_desc = data['order_description']
	total_price = 0
	total_tax = 0
	product_price = 0
	total_product_price = 0
	total_package_charge = 0
	for index in order_desc:
		pro_id = index['product_id']
		p_data = Product.objects.filter(id=pro_id)
		product_price = calculste_product_price(index)

	#	print("rrrrrrrrrrrrrrrrrrrrrr",product_price)




		tax = calculate_tax(pro_id,index['quantity'],product_price)
		package_charge = calculate_packagecharge(pro_id,product_price,index)
		total_product_price = float(total_product_price) + float(product_price)
		total_tax = total_tax + tax
		total_package_charge = total_package_charge + package_charge
	delivery_charge = calculate_deliverycharge(data['delivery_detail'],total_product_price)
	#print("kusum",total_product_price)


	final_result = {}
	if data['coupon_code'] == '':
		final_result['subtotal']       = total_product_price
		final_result['tax']            = total_tax
		final_result['delivery_charge'] = delivery_charge
		final_result['packing_charge'] = total_package_charge
		totalvalue = final_result['subtotal'] + final_result['tax'] + final_result['delivery_charge'] + final_result['packing_charge']

	else:
		tax,tdaprice = calculate_discount(data,data['coupon_code'])
		final_result['subtotal']        = total_product_price
		final_result['tax']             = tax
		final_result['delivery_charge'] = delivery_charge
		final_result['packing_charge']  = total_package_charge
		value = float(final_result['subtotal']) - float(tdaprice)
		totalvalue = value + final_result['tax'] + final_result['delivery_charge'] + final_result['packing_charge']
	
	print("subtotal",final_result['subtotal'])
	print("tax",final_result['tax'])
	print("delivery_charge",final_result['delivery_charge'])
	print("packing_charge",final_result['packing_charge'])
	print("total_value",totalvalue)


	return totalvalue






	




