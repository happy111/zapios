import re
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from Brands.models import Company
from _thread import start_new_thread
from datetime import datetime
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from Configuration.models import *
from ZapioApi.api_packages import *
from Location.models import *
from Product.models import Menu


class ConfigView(APIView):
	"""
	Configuration data listing GET API
		Authentication Required		: No
		Service Usage & Description	: This Api is used for providing config data of brand.
		Request param: url   (ex: url=sushijunction.aizotec.com)
		
	"""
	def get(self, request, format=None):
		try:
			# postdata = request.META
			url =["http://" + str(request.query_params["url"]),
				  "https://" + str(request.query_params["url"]),
				  str(request.query_params["url"])]
			url1 = url[1].split('.')[0]+'.in'
			if url:
				data = Company.objects.filter(Q(website__in=url)|Q(website=url1))
				#data = Company.objects.filter(id=13)
				if data.count()!=0:
					company_data = data[0]
					domain_name = addr_set()
					c_id = company_data.id
					country_id = company_data.country_id
					p_list={}
					pdata = []
					color_q = \
					ColorSetting.objects.filter(company=c_id,active_status=1)
					if color_q.count()!=0:
						p_list["accent_color"] = color_q[0].accent_color 
						p_list["textColor"] = color_q[0].textColor
						p_list["secondaryColor"] = color_q[0].secondaryColor
						p_list["brand_name"] = color_q[0].company.company_name
					else:
						return Response({"success": False,
							     "message":"Color Parameter is not set at super-admin level!!"})
					if company_data.company_logo != "" and company_data.company_logo != None:
						full_path = domain_name + str(company_data.company_logo)
						p_list['logo'] = full_path
					if company_data.company_landing_imge != "" and company_data.company_landing_imge != None:
						full_path1 = domain_name + str(company_data.company_landing_imge)
						p_list['banner'] = full_path1
					p_list['company'] = company_data.id
					p_list['order_source'] = []
					soucedata = OrderSource.objects.filter(active_status=1,company_id=c_id)
					if soucedata.count() > 0:
						for index in soucedata:
							souce_dict = {}
							souce_dict['id'] = index.id
							souce_dict['order_source'] = index.source_name
							p_list['order_source'].append(souce_dict)
					else:
						pass
					p_list['payment_mode'] = []
					paymentdata = PaymentMethod.objects.filter(active_status=1,company_id=c_id)
					if paymentdata.count() > 0:
						for index in paymentdata:
							payment_dict = {}
							payment_dict['id'] = index.id
							payment_dict['payment_method'] = index.payment_method
							payment_dict['keyid'] = index.keyid
							payment_dict['keySecret'] = index.keySecret
							p_list['payment_mode'].append(payment_dict)
					else:
						pass
					p_list['all_city'] = []

					allcity = CityMaster.objects.filter(active_status=1,company_id=c_id)
					if allcity.count() > 0:
						for j in allcity:
							city_dict = {}
							city_dict['id'] = j.id
							city_dict['city'] = j.city
							p_list['all_city'].append(city_dict)
					else:
						pass

					p_list['all_locality'] = []
					allcity = CityMaster.objects.filter(active_status=1,company_id=c_id)
					if allcity.count() > 0:
						for j in allcity:
							allarea = AreaMaster.objects.filter(active_status=1,city_id=j.id)
							for k in allarea:
								area_dict = {}
								area_dict['id'] = k.id
								area_dict['city'] = j.id
								area_dict['area'] = k.area
								p_list['all_locality'].append(area_dict)
					else:
						pass
					if company_data.facebook:
						p_list['facebook'] = company_data.facebook
					if company_data.instagram:
						p_list['instagram'] = company_data.instagram
					if company_data.twitter:
						p_list['twitter'] = company_data.twitter


					p_list['menu_url'] = []
					mdata = Menu.objects.filter(company_id=c_id)
					if mdata.count() > 0:
						for i in mdata:
							dic = {}
							dic['url'] = domain_name + str(i.menu_image)
							dic['id'] = str(i.id)
							p_list['menu_url'].append(dic)
					else:
						pass
					
					p_list['payment_method'] = []
					record = OnlinepaymentStatus.objects.filter(company=c_id,is_hide=0)
					if record.count() > 0:
						for q in record:
							q_dict = {}
							q_dict["id"] =  q.id
							q_dict["types"] =  q.types
							q_dict["payment_id"] =  q.payment_id
							q_dict["payment_method"] =  q.payment.payment_method
							q_dict['active_status'] = q.active_status
							p_list['payment_method'].append(q_dict)

					pdata.append(p_list)
					save_wev = WebsiteStatistic.objects.create(name=company_data.company_name,\
						visitors=1,company_id=company_data.id)
					
					pdata1 = DeliverySetting.objects.filter(company_id=c_id)
					if pdata1.count() > 0:
						dic1 = {}
						dic1['price_type'] = pdata1[0].price_type
						dic1['is_tax'] = pdata1[0].is_tax
						if dic1['is_tax'] == 1:
							t = pdata1[0].tax
							if t != None:
								if len(t) > 0:
									dic1['tax'] = []
									for i in t:
										d = {}
										ta = Tax.objects.filter(id=str(i))
										if ta.count() > 0:
											d['tax_name'] = ta[0].tax_name
											d['percentage'] = ta[0].tax_percent
											dic1['tax'].append(d)
								else:
									pass
							else:
								pass
						else:
							pass
						dic1['delivery_charge'] = pdata1[0].delivery_charge
						dic1['packing_charge'] = pdata1[0].package_charge
						pdata.append(dic1)
					else:
						pass

					return Response({"success":True,
								     "data":pdata,
								  
								     })
				else:
					return Response({"success":True,
								     "data":[]})
			else:
				return Response({"success": False,
							     "message":"Url not Found!!"})
		except Exception as e:
			print(e)
			return Response({"success": False,
							"message":"config api stucked into exception!!"})
