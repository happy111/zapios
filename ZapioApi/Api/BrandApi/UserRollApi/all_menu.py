from rest_framework.views import APIView
from rest_framework.response import Response
from UserRole.models import UserType
from rest_framework.permissions import IsAuthenticated
from UserRole.models import *
from Brands.models import Company
from django.db.models import Q
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user

class AllMenu(APIView):
	"""
	User listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of user type data within brand.
	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			auth_id = request.user.id
			Company_id = get_user(auth_id)
			userdata = UserType.objects.filter(active_status=1).order_by('id')
			udata = []
			for j in userdata:
				users = {}
				users['id'] = j.id
				users['user_type'] = j.user_type
				udata.append(users)
			
			allmenu = MainRoutingModule.objects.filter(active_status=1)
			alldatas = []
			for j in allmenu:
				users = {}
				main_id = j.id
				users['route'] = j.module_name
				users['ids'] = j.id
				users['id'] = j.module_id
				users['icon'] = j.icon
				users['label'] = j.label,
				users['rolls'] = []
				up = RollPermission.objects.filter(Q(user_type_id=10),\
					Q(main_route_id=main_id))
				if up.count() > 0:
					al = {}
					a = str(up[0].label)
					if a == 'False':
						al['label'] = "いいえ"
						al['value'] = str(0)
					else:
						al['label'] = "はい"
						al['value'] = str(1)
					users['types'] = up[0].user_type_id
					users['rolls'].append(al)
				alldatas.append(users)


			allmenu = MainRoutingModule.objects.filter(active_status=1)
			alldatass = []
			for j in allmenu:
				users = {}
				main_id = j.id
				users['route'] = j.module_name
				users['ids'] = j.id
				users['rolls'] = []
				up = RollPermission.objects.filter(Q(user_type_id=12),\
					Q(main_route_id=main_id))	
				if up.count() > 0:			
					al = {}
					a = str(up[0].label)
					if a == 'False':
						al['label'] = "いいえ"
						al['value'] = str(0)
					else:
						al['label'] = "はい"
						al['value'] = str(1)
					users['types'] = up[0].user_type_id
					users['rolls'].append(al)
				alldatass.append(users)



			# allmenu = MainRoutingModule.objects.filter(active_status=1)
			# alldatasss = []
			# for j in allmenu:
			# 	users = {}
			# 	main_id = j.id
			# 	users['route'] = j.module_name
			# 	users['ids'] = j.id
			# 	users['rolls'] = []
			# 	up = RollPermission.objects.filter(Q(user_type_id=3),Q(company_id=Company_id),\
			# 		Q(main_route_id=main_id))
			# 	if up.count() > 0:				
			# 		al = {}
			# 		a = str(up[0].label)
			# 		if a == 'False':
			# 			al['label'] = "No"
			# 			al['value'] = str(0)
			# 		else:
			# 			al['label'] = "Yes"
			# 			al['value'] = str(1)
			# 		users['types'] = up[0].user_type_id
			# 		users['rolls'].append(al)
			# 	alldatasss.append(users)


			# allmenu = MainRoutingModule.objects.filter(active_status=1)
			# admin = []
			# for j in allmenu:
			# 	users = {}
			# 	main_id = j.id
			# 	users['route'] = j.module_name
			# 	users['ids'] = j.id
			# 	users['rolls'] = []
			# 	up = RollPermission.objects.filter(Q(user_type_id=4),Q(company_id=Company_id),\
			# 		Q(main_route_id=main_id))
			# 	if up.count() > 0:				
			# 		al = {}
			# 		a = str(up[0].label)
			# 		if a == 'False':
			# 			al['label'] = "No"
			# 			al['value'] = str(0)
			# 		else:
			# 			al['label'] = "Yes"
			# 			al['value'] = str(1)
			# 		users['types'] = up[0].user_type_id
			# 		users['rolls'].append(al)
			# 	admin.append(users)



			# allmenu = MainRoutingModule.objects.filter(active_status=1)
			# omanager = []
			# for j in allmenu:
			# 	users = {}
			# 	main_id = j.id
			# 	users['route'] = j.module_name
			# 	users['ids'] = j.id
			# 	users['rolls'] = []
			# 	up = RollPermission.objects.filter(Q(user_type_id=5),Q(company_id=Company_id),\
			# 		Q(main_route_id=main_id))	
			# 	if up.count() > 0:			
			# 		al = {}
			# 		a = str(up[0].label)
			# 		if a == 'False':
			# 			al['label'] = "No"
			# 			al['value'] = str(0)
			# 		else:
			# 			al['label'] = "Yes"
			# 			al['value'] = str(1)
			# 		users['types'] = up[0].user_type_id
			# 		users['rolls'].append(al)
			# 	omanager.append(users)


			# allmenu = MainRoutingModule.objects.filter(active_status=1)
			# smanager = []
			# for j in allmenu:
			# 	users = {}
			# 	main_id = j.id
			# 	users['route'] = j.module_name
			# 	users['ids'] = j.id
			# 	users['rolls'] = []
			# 	up = RollPermission.objects.filter(Q(user_type_id=6),Q(company_id=Company_id),\
			# 		Q(main_route_id=main_id))
			# 	if up.count() > 0:
			# 		al = {}
			# 		a = str(up[0].label)
			# 		if a == 'False':
			# 			al['label'] = "No"
			# 			al['value'] = str(0)
			# 		else:
			# 			al['label'] = "Yes"
			# 			al['value'] = str(1)
			# 		users['types'] = up[0].user_type_id
			# 		users['rolls'].append(al)
			# 	smanager.append(users)



			# allmenu = MainRoutingModule.objects.filter(active_status=1)
			# amanager = []
			# for j in allmenu:
			# 	users = {}
			# 	main_id = j.id
			# 	users['route'] = j.module_name
			# 	users['ids'] = j.id
			# 	users['rolls'] = []
			# 	up = RollPermission.objects.filter(Q(user_type_id=7),Q(company_id=Company_id),\
			# 		Q(main_route_id=main_id))
			# 	if up.count() > 0:				
			# 		al = {}
			# 		a = str(up[0].label)
			# 		if a == 'False':
			# 			al['label'] = "No"
			# 			al['value'] = str(0)
			# 		else:
			# 			al['label'] = "Yes"
			# 			al['value'] = str(1)
			# 		users['types'] = up[0].user_type_id
			# 		users['rolls'].append(al)
			# 	amanager.append(users)


			# allmenu = MainRoutingModule.objects.filter(active_status=1)
			# cmanager = []
			# for j in allmenu:
			# 	users = {}
			# 	main_id = j.id
			# 	users['route'] = j.module_name
			# 	users['ids'] = j.id
			# 	users['rolls'] = []
			# 	up = RollPermission.objects.filter(Q(user_type_id=8),Q(company_id=Company_id),\
			# 		Q(main_route_id=main_id))
			# 	if up.count() > 0:				
			# 		al = {}
			# 		a = str(up[0].label)
			# 		if a == 'False':
			# 			al['label'] = "No"
			# 			al['value'] = str(0)
			# 		else:
			# 			al['label'] = "Yes"
			# 			al['value'] = str(1)
			# 		users['types'] = up[0].user_type_id
			# 		users['rolls'].append(al)
			# 	cmanager.append(users)


			# allmenu = MainRoutingModule.objects.filter(active_status=1)
			# fmanager = []
			# for j in allmenu:
			# 	users = {}
			# 	main_id = j.id
			# 	users['route'] = j.module_name
			# 	users['ids'] = j.id
			# 	users['rolls'] = []
			# 	up = RollPermission.objects.filter(Q(user_type_id=9),Q(company_id=Company_id),\
			# 		Q(main_route_id=main_id))				
			# 	al = {}
			# 	a = str(up[0].label)
			# 	if a == 'False':
			# 		al['label'] = "No"
			# 		al['value'] = str(0)
			# 	else:
			# 		al['label'] = "Yes"
			# 		al['value'] = str(1)
			# 	users['types'] = up[0].user_type_id
			# 	users['rolls'].append(al)
			# 	fmanager.append(users)


			# allmenu = MainRoutingModule.objects.filter(active_status=1)
			# mmanager = []
			# for j in allmenu:
			# 	users = {}
			# 	main_id = j.id
			# 	users['route'] = j.module_name
			# 	users['ids'] = j.id
			# 	users['rolls'] = []
			# 	up = RollPermission.objects.filter(Q(user_type_id=10),Q(company_id=Company_id),\
			# 		Q(main_route_id=main_id))
			# 	if up.count() > 0:				
			# 		al = {}
			# 		a = str(up[0].label)
			# 		if a == 'False':
			# 			al['label'] = "No"
			# 			al['value'] = str(0)
			# 		else:
			# 			al['label'] = "Yes"
			# 			al['value'] = str(1)
			# 		users['types'] = up[0].user_type_id
			# 		users['rolls'].append(al)
			# 	mmanager.append(users)
				



			# allmenu = MainRoutingModule.objects.filter(active_status=1)
			# staff = []
			# for j in allmenu:
			# 	users = {}
			# 	main_id = j.id
			# 	users['route'] = j.module_name
			# 	users['ids'] = j.id
			# 	users['rolls'] = []
			# 	up = RollPermission.objects.filter(Q(user_type_id=19),Q(company_id=Company_id),\
			# 		Q(main_route_id=main_id))
				
			# 	if up.count() > 0:				
			# 		al = {}
			# 		a = str(up[0].label)
			# 		if a == 'False':
			# 			al['label'] = "No"
			# 			al['value'] = str(0)
			# 		else:
			# 			al['label'] = "Yes"
			# 			al['value'] = str(1)
			# 		users['types'] = up[0].user_type_id
			# 		users['rolls'].append(al)
			# 	staff.append(users)
				

			return Response({
						"success": True,
						'usertype':udata,
						# "posmanager" : alldatas,
						# "salesmanager" : alldatass,
						# "cashier" : alldatasss,
						# "admin" : admin,
						"outletmanager" : alldatas,
						# "shiftmanager" : smanager,
						# "areamanager" : amanager,
						# "callmanager" : cmanager,
						# "financemanager" : fmanager,
						# "marketingmanager" : mmanager,
						"staff" : alldatass,
						})
		except Exception as e:
			print("UserType active listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
