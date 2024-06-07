from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from Product.models import Tag
from Brands.models import Company
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user




class ActiveTagList(APIView):

	"""
	Active Tag listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of Active Tag data.
	"""

	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			cid = request.user.id
			auth_id = request.user.id
			Company_id = get_user(auth_id)
			alltag = Tag.objects.filter(active_status=1)
			final_result = []
			if alltag.count() > 0:
				for i in alltag:
					alltag = {}
					alltag['tag_name'] = i.tag_name
					alltag['id'] = i.id
					final_result.append(alltag)
				return Response({
						"success": True, 
						"data": final_result})
			else:
				return Response({
						"success": True, 
						"data": []})
		except Exception as e:
			print("Active Tag listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})