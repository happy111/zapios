from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
#Serializer for api
from rest_framework import serializers
from django.db.models import Q
from datetime import datetime, timedelta
from urbanpiper.models import OutletSync, CatSync,ProductSync, ProductOutletWise
from Outlet.models import OutletProfile
from Product.models import ProductCategory, Product, Tag, Variant
from datetime import datetime
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user

def product_outletwise(sync_product_id,sync_outlet):
	query_check = ProductOutletWise.objects.filter(sync_product_id=sync_product_id,\
										sync_outlet_id=sync_outlet)
	if query_check.count() == 0:
		query_create = \
		ProductOutletWise.objects.create(sync_product_id=sync_product_id,\
					sync_outlet_id=sync_outlet,sync_status='not_intiated')
	else:
		query_update = \
		query_check.update(sync_status='not_intiated',is_enabled=0,is_available=0,\
			product_status='disabled',active_status=0,updated_at=datetime.now(),urban_event=None)
	return "created or updated"

class ProductAttach(APIView):
	"""
	Outletwise attach Product with urbanpiper POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for attaching Product to outlets with urbanpiper within brand.

		Data Post: {
			"outlet_id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "All Products are attached successfully!!"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			data = request.data
			auth_id = request.user.id
			Company_id = get_user(auth_id)
			record = OutletSync.objects.filter(outlet_id=data["outlet_id"],sync_status="synced")
			if record.count() == 0:
				return ({
					"status" : False,
					"message" : "This outlet is not valid to proceed!!"
					})
			else:
				product_q = Product.objects.filter(Company=Company_id,active_status=1)
				outlet_id = str(data["outlet_id"])
				sync_outlet = record[0].id
				sync_deactivate = ProductSync.objects.all().update(active_status=0)
				for q in product_q:
					sync_initial = ProductSync.objects.filter(product=q.id,\
						category=q.product_category_id)
					if q.has_variant == 0:
						sync_check = sync_initial
						if sync_check.count() == 0:
							price = float(q.price)
							discount_price = float(q.discount_price)
							outlet_map = [outlet_id]
							addon_group = q.addpn_grp_association
							addon_group = list(map(str, addon_group))
							sync_create = \
							ProductSync.objects.create(category_id = q.product_category_id,
									company_id = q.Company_id,price = price,
									discount_price = discount_price,
									product_id = q.id,\
									addpn_grp_association = addon_group,outlet_map = outlet_map,\
									active_status = 1)
							sync_product_id = sync_create.id
							product_outletwise(sync_product_id,sync_outlet)
						else:
							price = float(q.price)
							discount_price = float(q.discount_price)
							outlet_map = sync_check[0].outlet_map
							sync_id = sync_check[0].id
							addon_group = q.addpn_grp_association
							addon_group = list(map(str, addon_group))
							if outlet_id not in outlet_map:
								outlet_map.append(outlet_id)
							else:
								pass
							sync_update_record = sync_check.filter(id=sync_id)
							sync_update = \
								sync_update_record.update(category_id=q.product_category_id,\
								company_id=q.Company_id,price=price,\
								discount_price = discount_price,\
								product_id=q.id,\
								addpn_grp_association=addon_group,outlet_map=outlet_map,active_status=1,
								variant_id=None)
							sync_product_id = sync_check[0].id	
							product_outletwise(sync_product_id,sync_outlet)
					else:
						variant_deatils = q.variant_deatils
						outlet_map = [outlet_id]
						for i in variant_deatils:
							v_id = Variant.objects.filter(variant=i["name"])[0].id
							price = float(i["price"])
							discount_price = float(i["discount_price"])
							addon_group = i["addon_group"]
							addon_group = list(map(str, addon_group))
							sync_check = sync_initial.filter(variant=v_id)
							if sync_check.count() == 0:
								sync_create = \
								ProductSync.objects.create(category_id=q.product_category_id,\
								company_id=q.Company_id,variant_id=v_id,price=price,\
								discount_price = discount_price,\
								product_id=q.id,\
								addpn_grp_association=addon_group,outlet_map=outlet_map,active_status=1)
								sync_product_id = sync_create.id
								product_outletwise(sync_product_id,sync_outlet)
							else:
								# sync_check = sync_initial.filter(variant=v_id)
								outlet_map = sync_check[0].outlet_map
								if outlet_id not in outlet_map:
									outlet_map.append(outlet_id)
								else:
									pass
								sync_update = \
								sync_check.update(category_id=q.product_category_id,\
								company_id=q.Company_id,variant_id=v_id,price=price,\
								discount_price = discount_price,\
								product_id=q.id,\
								addpn_grp_association=addon_group,outlet_map=outlet_map,active_status=1)
								sync_product_id = sync_check[0].id
								product_outletwise(sync_product_id,sync_outlet)
				query_update = \
					ProductOutletWise.objects.filter(sync_outlet_id=sync_outlet).\
					update(is_enabled=0,is_available=0,active_status=0)
				sync_count = ProductOutletWise.objects.filter(sync_outlet_id=sync_outlet).count()								
				if sync_count == 0:
					msg = "Products are already attached!!"
				else:
					msg = "Total "+str(sync_count) +" products are attached!!"
			return Response({"status": True,
							"message" : msg})
		except Exception as e:
			print(e)
			return Response(
						{"error":str(e)}
						)
