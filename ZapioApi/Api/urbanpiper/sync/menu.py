from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Brands.models import Company
#Serializer for api
from rest_framework import serializers
from django.db.models import Q
from datetime import datetime, timedelta
from urbanpiper.models import OutletSync, UrbanCred, APIReference, EventTypes, CatSync, \
ProductOutletWise,ProductSync,CatOutletWise, MenuPayload
from Outlet.models import OutletProfile
from datetime import datetime, timedelta
import requests
import json
from zapio.settings import Media_Path
from Product.models import Variant, AddonDetails, Addons
from Configuration.models import DeliverySetting
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user

def menu_sync(data,company_id, outlet_id):
	url = "https://api.urbanpiper.com/external/api/v1/inventory/locations/"+str(outlet_id)+"/"
	data = data
	q = UrbanCred.objects.filter(company_id=company_id,active_status=1)
	if q.count() == 0:
		return None
	else:
		apikey = q[0].apikey
		username = q[0].username
		headers = {}
		headers["Authorization"] = "apikey "+ username +":"+apikey
		headers["Content-Type"] = "application/json"
		response = requests.request("POST", url, data=json.dumps(data), headers=headers)
		response_data = response.json()
		event_type_q = EventTypes.objects.filter(company=company_id,event_type="inventory_update")
		if event_type_q.count() == 0:
			return None
		else:
			event_type_id = event_type_q[0].id
		if response_data["status"] != "error":
			record_create = \
			APIReference.objects.create(company_id=company_id,event_type_id=event_type_id,\
											ref_id=response_data["reference"],
											api_response=response_data,outlet_id=outlet_id)
		else:
			record_create = \
			APIReference.objects.create(company_id=company_id,event_type_id=event_type_id,\
											ref_id=response_data["reference"],
											error_api_response=response_data,outlet_id=outlet_id)
		return response_data





class MenuSync(APIView):
	"""
	Outletwise Menu Syncing POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for syncing menus outletwise with UrbanPiper.

		Data Post: {
			"outlet_id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "Syncing of menu is initiated successfully!!"
		}
	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			data = request.data
			auth_id = request.user.id
			Company_id = get_user(auth_id)
			record = OutletSync.objects.filter(company=Company_id, sync_status='synced',\
									outlet=data["outlet_id"],outlet__active_status=1)
			if record.count() == 0:
				return Response({
					"status" : True,
					"message" : "Outlet is not valid to proceed!!"
					})
			else:
				company_id = Company_id
				outlet_id = data["outlet_id"]
			data = request.data
			sync_data = {}
			sync_data["flush_items"] = True
			sync_data["flush_options"] = True
			sync_data["flush_option_groups"] = True
			sync_data["categories"] = []
			sync_data["items"] = []
			sync_data["option_groups"] = []
			sync_data["options"] = []
			sync_data["taxes"] = []
			sync_data["charges"] = []
			cat_q = CatSync.objects.filter(category__active_status=1)
			if cat_q.count() == 0:
				return Response({
					"status":False,
					"message" : "No categories are attached!!"
					})
			else:
				for q in cat_q:
					cat_dict = {}
					cat_dict["ref_id"] = "C-"+str(q.category_id)
					cat_dict["name"] = q.category.category_name
					cat_dict["description"] = q.category.description
					cat_dict["sort_order"] = q.category.priority
					if cat_dict["sort_order"] == None:
						cat_dict["sort_order"] = 0
					else:
						pass
					cat_dict["active"] = True
					cat_dict["img_url"] = None
					cat_dict["parent_ref_id"] = None
					cat_dict["translations"] = []
					cat_dict["language"] = []
					sync_data["categories"].append(cat_dict)
					cat_update = CatOutletWise.objects.\
					filter(sync_cat=q.id,sync_outlet__outlet=outlet_id).\
					update(sync_status="in_progress")
			product_q = ProductSync.objects.filter(product__active_status=1,active_status=1)
			cid = product_q[0].company_id
			if product_q.count() == 0:
				return Response({
					"status":False,
					"message" : "No products are attached!!"
					})
			else:
				item_ids = []
				addon_grp = []
				for i in product_q:
					if i.price != 0.0:
						product_dict = {}
						product_dict["ref_id"] = "I-"+str(i.id) 
						item_ids.append(product_dict["ref_id"])
						product_dict["title"] = i.product.product_name
						if i.variant == None:
							pass
						else:
							product_dict["title"] = i.product.product_name + " | " + i.variant.variant  
						product_dict["price"] = i.price
						product_dict["description"] = i.product.product_desc
						product_dict["sold_at_store"] = True
						product_dict["available"] = True
						product_dict["sort_order"] = i.product.priority
						product_dict["current_stock"] = -1
						product_dict["category_ref_ids"] = []
						product_dict["category_ref_ids"].append("C-"+str(i.category_id))
						product_dict["food_type"] = i.product.food_type.food_type
						if product_dict["food_type"] == "Vegetarian":
							product_dict["food_type"] = 1
						else:
							product_dict["food_type"] = 2
						product_dict['img_url'] = i.product.product_image
						if product_dict['img_url'] != None and product_dict['img_url'] != "" and\
							product_dict['img_url'] != "null":
							product_dict['img_url'] = Media_Path+str(i.product.product_image)
						else:
							product_dict['img_url'] = None
						product_dict["recommended"] = True
						product_dict["translations"] = []
						product_dict["language"] = []
						# if product_dict["price"] < 150:
						# 	product_dict["excluded_platforms"] = ["zomato"]
						# 	product_dict["included_platforms"] = ["swiggy"]
						# 	product_dict["tags"] = {}
						# 	product_dict["tags"]["swiggy"] = ["treat", "deal150"]
						# else:
						# 	product_dict["tags"] = {}
						# 	# product_dict["excluded_platforms"] = []
						# 	product_dict["included_platforms"] = ["swiggy","zomato"]
						product_dict["tags"] = {}
						product_dict["excluded_platforms"] = []
						product_dict["included_platforms"] = ["swiggy","zomato"]
						sync_data["items"].append(product_dict)
						product_update = ProductOutletWise.objects.\
						filter(sync_product=i.id,sync_outlet__outlet=outlet_id).\
						update(sync_status="in_progress")
						associate_addon_grp = i.addpn_grp_association
						for j in  associate_addon_grp:
							if j not in addon_grp:
								addon_group = AddonDetails.objects.filter(active_status=1,Company_id=cid,\
													id=str(j))
								if addon_group.count() != 0:
									addon_grp.append(j)
								else:
									pass
							else:
								pass
					else:
						pass
			addon_grp_q = AddonDetails.objects.filter(active_status=1,Company_id=cid)
			for k in addon_grp_q:
				product_check = product_q.filter(addpn_grp_association__contains=[str(k.id)])
				if product_check.count() != 0:
					addon_grp_dict = {}
					query = addon_grp_q.filter(id=k.id)[0]
					if query.associated_addons != None and len(query.associated_addons) != 0: 
						addon_grp_dict["ref_id"] = "AG-"+str(query.id)
						addon_grp_dict["title"] = query.addon_gr_name
						addon_grp_dict["description"] = None
						addon_grp_dict["min_selectable"] = query.min_addons
						addon_grp_dict["max_selectable"] = query.max_addons
						addon_grp_dict["sort_order"] = 0
						addon_grp_dict["active"] = True
						addon_grp_dict["display_inline"] = True
						addon_grp_dict["item_ref_ids"] = []
						for l in product_check:
							item_id = "I-"+str(l.id) 
							if item_id not in addon_grp_dict["item_ref_ids"]:
								addon_grp_dict["item_ref_ids"].append(item_id)
							else:
								pass
						addon_grp_dict["translations"] = []
						addon_grp_dict["language"] = []
						sync_data["option_groups"].append(addon_grp_dict)
					else:
						pass
				else:
					pass
			for m in addon_grp:
				addon_q = Addons.objects.filter(active_status=1,addon_group_id=m)
				for n in addon_q:
					addon_dict = {}
					addon_dict["ref_id"] = "A-"+str(n.id)
					addon_dict["title"] = n.name
					addon_dict["price"] = n.addon_amount
					addon_dict["description"] = None
					addon_dict["available"] = True
					addon_dict["sold_at_store"] = True
					addon_dict["food_type"] = 1
					addon_dict["translations"] = []
					addon_dict["opt_grp_ref_ids"] = []
					addon_dict["opt_grp_ref_ids"].append("AG-"+str(m))
					addon_dict["nested_opt_grps"] = []
					addon_dict["language"] = []
					sync_data["options"].append(addon_dict)
			# tax_record = DeliverySetting.objects.filter(company=cid)
			# if tax_record.count() == 0:
			# 	return Response({
			# 				"status":True,
			# 				"message" : "Tax is not properly configured at super-admin level!!"
			# 				})
			# else:
			# 	pass
			# t = tax_record[0]
			# # for cgst
			# tax_dict = {}
			# tax_dict["ref_id"] = str(outlet_id)+"-cgst"+str(t.id)
			# tax_dict["title"] = "CGST"
			# tax_dict["description"] = "2.5% CGST on all items"
			# tax_dict["active"] =  True
			# tax_dict["structure"] = {}
			# tax_dict["structure"]["type"] = "percentage"
			# tax_dict["structure"]["applicable_on"] = "item.price"
			# tax_dict["structure"]["value"] = t.CGST
			# tax_dict["item_ref_ids"] = item_ids
			# sync_data["taxes"].append(tax_dict)

			# # for sgst
			# tax_dict = {}
			# tax_dict["ref_id"] = str(outlet_id)+"-sgst"+str(t.id)
			# tax_dict["title"] = "SGST"
			# tax_dict["description"] = "2.5% SGST on all items"
			# tax_dict["active"] =  True
			# tax_dict["structure"] = {}
			# tax_dict["structure"]["type"] = "percentage"
			# tax_dict["structure"]["applicable_on"] = "item.price"
			# tax_dict["structure"]["value"] = t.tax_percent
			# tax_dict["item_ref_ids"] = item_ids
			# sync_data["taxes"].append(tax_dict)

			# for charges
			# charge_dict = {}
			# charge_dict["ref_id"] = str(outlet_id)+"-PC"+str(t.id)
			# charge_dict["title"] = "Packing Charge"
			# charge_dict["description"] = "Packing Charge per Item Quantity"
			# charge_dict["active"] = True
			# charge_dict["structure"] = {}
			# charge_dict["structure"]["type"] = "fixed"
			# charge_dict["structure"]["applicable_on"] = "item.quantity"
			# charge_dict["structure"]["value"] = t.package_charge
			# charge_dict["fulfillment_modes"] = ["delivery"]
			# charge_dict["excluded_platforms"] = []
			# charge_dict["item_ref_ids"] = item_ids
			# sync_data["charges"].append(charge_dict)

			urban_sync = menu_sync(sync_data,company_id, outlet_id)
			payload_create = \
			MenuPayload.objects.create(company_id=company_id,outlet_id=outlet_id, payload=sync_data)
			if urban_sync == None:
				cat_revert = CatOutletWise.objects,filter(sync_outlet__outlet=outlet_id).\
				update(sync_status='not_intiated')
				product_revert =  ProductOutletWise.objects,filter(sync_outlet__outlet=outlet_id).\
				update(sync_status='not_intiated')
				return Response({
							"status":False,
							"message" : "Syncing of outletwise menu is not initiated successfully!!"
							})
			else:
				pass
			return Response({
							"status":True,
							"message" : "Syncing of menu is initiated successfully!!"
							})
		except Exception as e:
			print(e)
			return Response(
						{"error":str(e)}
						)


