from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from Product.models import *
from Outlet.models import OutletProfile
from Brands.models import Company
from ZapioApi.api_packages import *
from UserRole.models import * 
from django.db.models import Q
from frontApi.menu.customize_fun import CustomizeProduct
import datetime
from discount.models import Coupon
from Configuration.models import TaxSetting
from zapio.settings import Media_Path



def POSProductAvailableList(data,user):
	err_message = {}
	err_message["outlet"] = \
			validation_master_anything(str(data["outlet"]),
			"Outlet",contact_re, 1)
	if any(err_message.values())==True:
		err = {
			"success": False,
			"error" : err_message,
			"message" : "Please correct listed errors!!"
			}
		return err
	outlet = OutletProfile.objects.filter(id=data["outlet"],active_status=1)
	user_id = user.id
	co_id = outlet[0].Company_id
	chk_outlet = OutletProfile.objects.filter(Q(Company_id=co_id),Q(id=data['outlet']))
	if chk_outlet.count() > 0:
		pass
	else:
		err = {
			"success": False,
			"error" : err_message,
			"message" : "Outlet ID is not found!!"
			}
		return err
	cat_q = Category_availability.objects.filter(outlet_id=data["outlet"])
	if len(cat_q[0].available_cat) > 0:
		pass
	else:
		err = {
			"success":False,
			"message":"No Category available!!",
			"data":[]
			}
		return err
	product_q = Product_availability.objects.filter(outlet_id=data["outlet"])
	final_result = []
	coupons = {}
	coupons["coupon_details"] = []
	today = datetime.datetime.now()
	query = Coupon.objects.filter(frequency__gte=1,
						valid_till__gte=today,outlet_id__icontains=str(data["outlet"]))
	if query.count() > 0:
		for i in query:
			coupon = {}
			coupon['coupon_type'] = i.coupon_type
			coupon['coupon_code'] = i.coupon_code
			coupon['frequency'] = i.frequency
			coupon['valid_frm'] = i.valid_frm.strftime("%d/%b/%Y %I:%M %p")
			coupon['valid_till'] = i.valid_till.strftime("%d/%b/%Y %I:%M %p")
			if len(i.product_map) > 0:
				coupon['product'] = []
				a = i.product_map
				for j in range(len(i.product_map)):
					pro = {}
					pro['id'] = a[j]
					pro['product_name'] = Product.objects.filter(id=a[j])[0].product_name
					coupon['product'].append(pro)
			else:
				pass
			coupons["coupon_details"].append(coupon)
	else:
		pass
	final_result.append(coupons)

	if product_q.count() > 0:
		company_id = Company.objects.filter(id=co_id)[0].id
		outlet_id = data["outlet"]
		product = Product.objects.filter(active_status=1,Company=co_id)
		product_ids = product_q[0].available_product
		if len(product_ids) != 0:
			for p in product_ids:
				product_dict = {}
				product_dict["id"] = p
				chk_p = Product.objects.filter(id=p,active_status=1,is_hide=0)
				if chk_p.count() > 0:
					pobj = Product.objects.filter(id=p)[0]
					product_dict["product_name"] = pobj.product_name
					product_dict["food_type"] = pobj.food_type.food_type
					product_dict["priority"] = pobj.priority
					product_dict["sku"] = pobj.product_code
					product_dict["ordering_code"] = pobj.ordering_code
					p_img = ProductImage.objects.filter(product_id=pobj.id,primary_image=1)
					if p_img.count() > 0:
						product_dict['primary_image'] = Media_Path+str(p_img[0].product_image)
					else:
						product_dict['primary_image'] = ''
					if pobj.price == 0:
						a = pobj.variant_deatils
						if a !=None:
							c = []
							d = []
							for i in a:
								c.append(i['price'])
								d.append(i['discount_price'])
							product_dict["price"] = min(c)
							product_dict["dis_price"] = min(d)
							product_dict["fprice"] = 0
						else:
							product_dict["price"] = 0
							product_dict["fprice"] = 0
					else:
						product_dict["price"] = pobj.price
						product_dict["fprice"] = pobj.discount_price

					product_dict["description"] = pobj.product_desc
					product_dict["kot_desc"] = pobj.kot_desc
					product_dict["tag"] = []
					product_dict["tags"] = []
					tag_chk = pobj.tags
					if isinstance(tag_chk, list):
						for i in range(len(tag_chk)):
							tagg = {}
							tagg['name'] = Tag.objects.filter(id=tag_chk[i])[0].tag_name
							tagg['id']   = Tag.objects.filter(id=tag_chk[i])[0].id
							product_dict["tag"].append(tagg)
							product_dict["tags"].append(tagg['name'])
					else:
						pass
					product_dict["allergen_information"] = pobj.allergen_Information
					product_dict["spice"] = pobj.spice
					product_dict["available_for"] = {}
					d =  pobj.delivery_option
					if d != None:
						if len(d) > 0:
							product_dict["available_for"]['isDineIn']   = d[0]['isDineIn']
							product_dict["available_for"]['isDelivery'] = d[0]['isDelivery']
							product_dict["available_for"]['isTakeaway'] = d[0]['isTakeaway']
							product_dict["available_for"]['isViewOnly'] = d[0]['isViewOnly']
					else:
						pass
					q = Product.objects.filter(id=pobj.id)
					if q.count() > 0:
						product_dict["category_id"] = q[0].product_categorys
					else:
						product_dict['category_id'] = []
					if str(p) not in product_ids:
						product_dict["is_available"] = False
					else:
						product_dict["is_available"] = True
					p_list = {}
					p_list['p_id'] = p
					product_dict['customize_detail'] = CustomizeProduct(p_list)
					product_dict["tax_detail"] = []
					associate_tax = pobj.tax_association
					if associate_tax != None:
						if len(associate_tax) == 0:
							pass
						else:
							for t in associate_tax:
								tax_dict = {}
								ts = TaxSetting.objects.filter(id=t)
								if ts.count() > 0:
									tax_q = ts[0]
									tax_dict["id"] = tax_q.id
									tax_dict["tax_name"] = tax_q.tax_name+" | "+str(tax_q.tax_percent)
									tax_dict["tax_percent"] = tax_q.tax_percent
									product_dict["tax_detail"].append(tax_dict)
								else:
									pass
					else:
						pass
					final_result.append(product_dict)
				else:
					pass
		else:
			pass
	else:
		pass
	if len(final_result) > 0:
		err = {
			"success":True,
			"message":"Outletwise product listing worked well!!",
			"data":final_result
			}
	else:
		err = {
			"success":True,
			"message":"Outletwise product listing worked well!!",
			"data":final_result
		}
	return err

def POSCategoryAvailableList(data,user):
	err_message = {}
	err_message["outlet"] = \
			validation_master_anything(str(data["outlet"]),
			"Outlet",contact_re, 1)
	if any(err_message.values())==True:
		err = {
			"success": False,
			"error" : err_message,
			"message" : "Please correct listed errors!!"
			}
		return Response(err)
	outlet = OutletProfile.objects.filter(id=data["outlet"],active_status=1)
	if outlet.count() == 0:
		return None
	else:
		user_id = user.id
		co_id = outlet[0].Company_id
		chk_outlet = OutletProfile.objects.filter(Q(Company_id=co_id),Q(id=data['outlet']))
		if chk_outlet.count() > 0:
			pass
		else:
			err = {
				"success": False,
				"error" : err_message,
				"message" : "Outlet ID is not found!!"
				}
			return err
		co_id = ManagerProfile.objects.filter(auth_user_id=user_id)[0].Company_id
		cat_q = Category_availability.objects.filter(outlet_id=data["outlet"])
		company_id = Company.objects.filter(id=co_id)[0].id
		category = ProductCategory.objects.filter(active_status=1,Company=company_id)
		
		print("vvvvvvvvvvvvvvvvvv",category)

		final_result = []
		if cat_q.count() == 0:
			create_cat_avail = \
			Category_availability.objects.create(outlet_id=data["outlet"],available_cat=[])
			for p in category:
				cat_dict = {}
				cat_dict["id"] = p.id
				cat_dict["category_name"] = p.category_name
				cat_dict["category_code"] = p.category_code
				cat_dict["priority"] = p.priority
				cat_dict["is_available"] = False
				final_result.append(cat_dict)
		else:
			cat_ids = cat_q[0].available_cat
			if len(cat_ids) != 0:
				for p in cat_ids:
					chk_p = ProductCategory.objects.filter(id=p,active_status=1)
					if chk_p.count() > 0:
						cat_dict = {}
						cat_dict["id"] = p
						cat_dict["category_name"] = chk_p[0].category_name
						cat_dict["category_code"] = chk_p[0].category_code
						cat_dict["priority"] = chk_p[0].priority
						if str(p) not in cat_ids:
							cat_dict["is_available"] = False
						else:
							cat_dict["is_available"] = True
						final_result.append(cat_dict)
					else:
						pass
			else:
				pass
	if len(final_result) > 0:
		err = {
			"success":True,
			"message":"Outletwise category listing worked well!!",
			"data":final_result
			}
	else:
		err = {
			"success":True,
			"message":"Outletwise category listing worked well!!",
			"data":final_result
			}
	return err
