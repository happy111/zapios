import json
import math
import dateutil.parser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.db.models import Q
from datetime import datetime, timedelta
from ZapioApi.api_packages import *
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from Brands.models import Company
from UserRole.models import ManagerProfile
from Orders.models import Order,OrderStatusType,OrderTracking
from django.http import HttpResponse
from Outlet.models import OutletProfile


class StaffListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerProfile
        fields = "__all__"


class Allrider(ListAPIView):
    """
	Attandance data get API

		Authentication Required		 	: 		Yes
		Service Usage & Description	 	: 		This Api is used to provide listing rider all information.

	"""

    permission_classes = (IsAuthenticated,)
    serializer_class = StaffListSerializer
    queryset = ManagerProfile.objects.all()

    def get_queryset(self):
        data = self.request.query_params
        cid = get_user(self.request.user.id)
        queryset = []
        queryset = ManagerProfile.objects.filter(
            is_rider=1,
            active_status=1,
            Company_id=cid
        ).order_by('manager_name')
        return queryset



class RiderCsv(APIView):
    """
    Rider Report  data GET API

        Authentication Required     : Yes
        Service Usage & Description : .Download Rider csv file

        Data Post: {
        }

        Response: {

            "success": True, 
            "message": "Rider Report Download api worked well!!",
            "data": final_result
        }

    """
    # permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
            s_date = request.GET.get('start_date')
            e_date = request.GET.get('end_date')
            start_date = dateutil.parser.parse(s_date)
            end_date = dateutil.parser.parse(e_date)
            token = request.GET.get('token')
            user = Token.objects.filter(key=token)[0].user_id
            cid = get_user(user)
            report_type = request.GET.get('type')
            if report_type == 'consoledate':
                data = Order.objects.filter(Q(order_time__lte=end_date),Q(order_time__gte=start_date)
                        ,Q(Company_id=cid),Q(is_rider_assign=1))
                import xlwt
                response = HttpResponse(content_type='application/ms-excel')
                response['Content-Disposition'] = 'attachment; filename=rider_reports.xls'
                wb = xlwt.Workbook(encoding='utf-8')
                ws = wb.add_sheet("rider_reports")
                ws.write(0, 0, 'Start Date',xlwt.easyxf('align:horiz centre; pattern: pattern solid, fore_color orange;  font: color white,bold on,height 200'))
                ws.write(0, 1, s_date)
                ws.write(0, 2, 'End Date',xlwt.easyxf('align:horiz centre; pattern: pattern solid, fore_color orange;  font: color white,bold on,height 200'))
                ws.write(0, 3, e_date)
                font_style = xlwt.XFStyle()
                font_style.font.bold = True
                pattern = xlwt.Pattern()
                pattern.pattern = xlwt.Pattern.SOLID_PATTERN
                pattern.pattern_fore_colour = xlwt.Style.colour_map['blue']  # Set the cell background color to yellow
                font_style.pattern = pattern
                font_style = xlwt.XFStyle()
                font_style.alignment.wrap = 1
                date_format = xlwt.XFStyle()
                date_format.num_format_str = 'dd/mm/yyyy'

                row_num = 2
                columns = [
                    ("Order Date", 4000),
                    ("Order Time", 4000),
                    ("Order ID", 7000),
                    ("Outlet Name", 4000),
                    ("Rider Name", 4000),
                    ("Rider Mobile", 4000),
                    ("Dispatch Time", 3000),
                    ("Predicted KM", 3500),
                    ("Entered KM", 3500),
                    ("Rate per km", 3500),
                    ("Delivery Cost",3500),
                    ("Total Amount", 4000),
                  ]
                font_style = xlwt.XFStyle()
                font_style.font.bold = True
                for col_num in range(len(columns)):
                    ws.write(row_num, col_num, columns[col_num][0], font_style)
                    ws.col(col_num).width = columns[col_num][1]
                font_style = xlwt.XFStyle()
                font_style.alignment.wrap = 1
                ord_data =[]  
                tprice = 0
                if data.count() > 0:
                    for i in data:
                        p_list = {}
                        p_list['order_time'] = i.order_time
                        p_list['outlet_order_id'] = i.outlet_order_id
                        p_list['amount'] = i.total_bill_value
                        p_list['distance'] = i.distance
                        outlet_id = i.outlet_id
                        if outlet_id !=None:
                            p_list['outlet_name'] = OutletProfile.objects.filter(id=outlet_id)[0].Outletname
                        else:
                             p_list['outlet_name'] = 'N/A'
                        rider_data = ManagerProfile.objects.filter(id=i.delivery_boy_id)
                        if rider_data.count() > 0:
                            p_list['name']   = rider_data[0].manager_name + '' + rider_data[0].last_name
                            p_list['mobile'] = rider_data[0].mobile
                            p_list['compensation'] = rider_data[0].compensation
                            p_list['km'] = rider_data[0].km
                        else:
                            p_list['name'] = ''
                            p_list['mobile'] = ''
                            p_list['compensation'] = ''
                            p_list['km'] = ''
                        track_order = OrderTracking.objects.filter(Q(order_id=i.id),\
                                        Q(Order_staus_name_id=1))
                        if track_order.count() > 0:
                            o = track_order[0].created_at
                            q = o+timedelta(hours=5,minutes=30)
                            s = q.time()
                            a = str(s).split('.')
                            frd = a[0]
                        else:
                            frd = 'N/A'
                        atimes = OrderTracking.objects.filter(Q(order_id=i.id),\
                                        Q(Order_staus_name_id=2))
                        if atimes.count() > 0:
                            o = atimes[0].created_at
                            q = o+timedelta(hours=5,minutes=30)
                            s = q.time()
                            a = str(s).split('.')
                            act = a[0]
                        else:
                            act = 'N/A'
                        fready = OrderTracking.objects.filter(Q(order_id=i.id),\
                                        Q(Order_staus_name_id=3))
                        if fready.count() > 0:
                            o = fready[0].created_at
                            q = o+timedelta(hours=5,minutes=30)
                            s = q.time()
                            a = str(s).split('.')
                            fredy = a[0]
                        else:
                            fredy = 'N/A'
                        disp = OrderTracking.objects.filter(Q(order_id=i.id),\
                                        Q(Order_staus_name_id=4))
                        if disp.count() > 0:
                            o = disp[0].created_at
                            q = o+timedelta(hours=5,minutes=30)
                            s = q.time()
                            a = str(s).split('.')
                            dredy = a[0]
                        else:
                            dredy = 'N/A'
                        delivered = OrderTracking.objects.filter(Q(order_id=i.id),\
                                        Q(Order_staus_name_id=5))
                        if delivered.count() > 0:
                            o = delivered[0].created_at
                            q = o+timedelta(hours=5,minutes=30)
                            s = q.time()
                            a = str(s).split('.')
                            delivered_time = a[0]
                            d_time     = o+timedelta(hours=5,minutes=30)
                            dtime = str(d_time.strftime("%I:%M %p"))
                            p_list['dispatch_time'] = dtime
                        else:
                            delivered_time = 'N/A'
                            p_list['dispatch_time'] = ''
                        # if disp.count() > 0 and delivered.count() > 0:
                        #     date_format = "%H:%M:%S"
                        #     t1 = datetime.strptime(str(dredy),date_format)
                        #     t2 = datetime.strptime(str(delivered_time),date_format)
                        #     f = t2 - t1
                        #     sec = f.total_seconds()
                        #     ddiff = f
                        #     p_list['delivered_time'] = ddiff
                        # else:
                        #     p_list['delivered_time'] = 'N/A'
                        ord_data.append(p_list)
                for obj in ord_data:
                    row_num += 1
                    o_time = obj['order_time']+timedelta(hours=5,minutes=30)
                    order_time = str(o_time.strftime("%I:%M %p"))
                    order_date = str(o_time.strftime("%d/%b/%y"))
                    if obj['compensation'] != None:
                        delivery_cost = obj['distance'] * obj['compensation']
                    else:
                        delivery_cost = 0
                    row = [
                        order_date,
                        order_time,
                        obj['outlet_order_id'],
                        obj['outlet_name'],
                        obj['name'],
                        obj['mobile'],
                        obj['dispatch_time'],
                        obj['distance'],
                        obj['distance'],
                        obj['compensation'],
                        delivery_cost,
                        obj['amount']
                    ]
                    for col_num in range(len(row)):
                        ws.write(row_num, col_num, row[col_num], font_style)
                wb.save(response)
                return response
            else:
                pass

            if report_type == 'rider':
                data = Order.objects.filter(Q(order_time__lte=end_date),Q(order_time__gte=start_date)
                        ,Q(Company_id=cid),Q(is_rider_assign=1))
                import xlwt
                response = HttpResponse(content_type='application/ms-excel')
                response['Content-Disposition'] = 'attachment; filename=rider_reports.xls'
                wb = xlwt.Workbook(encoding='utf-8')
                ws = wb.add_sheet("rider_reports")
                ws.write(0, 0, 'Start Date',xlwt.easyxf('align:horiz centre; pattern: pattern solid, fore_color orange;  font: color white,bold on,height 200'))
                ws.write(0, 1, s_date)
                ws.write(0, 2, 'End Date',xlwt.easyxf('align:horiz centre; pattern: pattern solid, fore_color orange;  font: color white,bold on,height 200'))
                ws.write(0, 3, e_date)
                font_style = xlwt.XFStyle()
                font_style.font.bold = True
                pattern = xlwt.Pattern()
                pattern.pattern = xlwt.Pattern.SOLID_PATTERN
                pattern.pattern_fore_colour = xlwt.Style.colour_map['blue']  # Set the cell background color to yellow
                font_style.pattern = pattern
                font_style = xlwt.XFStyle()
                font_style.alignment.wrap = 1
                date_format = xlwt.XFStyle()
                date_format.num_format_str = 'dd/mm/yyyy'

                row_num = 2
                columns = [
                    ("Order Date", 4000),
                    ("Order Time", 4000),
                    ("Order ID", 7000),
                    ("Outlet Name", 4000),
                    ("Rider Name", 4000),
                    ("Rider Mobile", 4000),
                    ("Dispatch Time", 3000),
                    ("Predicted KM", 12000),
                    ("Entered KM", 4000),
                    ("Compensation Rate", 5000),
                    ("Total Amount", 4000),
                  ]
                font_style = xlwt.XFStyle()
                font_style.font.bold = True
                for col_num in range(len(columns)):
                    ws.write(row_num, col_num, columns[col_num][0], font_style)
                    ws.col(col_num).width = columns[col_num][1]
                font_style = xlwt.XFStyle()
                font_style.alignment.wrap = 1
                ord_data =[]  
                tprice = 0
                if data.count() > 0:
                    for i in data:
                        p_list = {}
                        p_list['order_time'] = i.order_time
                        p_list['outlet_order_id'] = i.outlet_order_id
                        p_list['amount'] = i.total_bill_value
                        p_list['distance'] = i.distance
                        outlet_id = i.outlet_id
                        if outlet_id !=None:
                            p_list['outlet_name'] = OutletProfile.objects.filter(id=outlet_id)[0].Outletname
                        else:
                             p_list['outlet_name'] = 'N/A'
                        rider_data = ManagerProfile.objects.filter(id=i.delivery_boy_id)
                        if rider_data.count() > 0:
                            p_list['name']   = rider_data[0].manager_name + '' + rider_data[0].last_name
                            p_list['mobile'] = rider_data[0].mobile
                            p_list['compensation'] = rider_data[0].compensation
                            p_list['km'] = rider_data[0].km
                        else:
                            p_list['name'] = ''
                            p_list['mobile'] = ''
                            p_list['compensation'] = ''
                            p_list['km'] = ''
                        track_order = OrderTracking.objects.filter(Q(order_id=i.id),\
                                        Q(Order_staus_name_id=1))
                        if track_order.count() > 0:
                            o = track_order[0].created_at
                            q = o+timedelta(hours=5,minutes=30)
                            s = q.time()
                            a = str(s).split('.')
                            frd = a[0]
                        else:
                            frd = 'N/A'
                        atimes = OrderTracking.objects.filter(Q(order_id=i.id),\
                                        Q(Order_staus_name_id=2))
                        if atimes.count() > 0:
                            o = atimes[0].created_at
                            q = o+timedelta(hours=5,minutes=30)
                            s = q.time()
                            a = str(s).split('.')
                            act = a[0]
                        else:
                            act = 'N/A'
                        fready = OrderTracking.objects.filter(Q(order_id=i.id),\
                                        Q(Order_staus_name_id=3))
                        if fready.count() > 0:
                            o = fready[0].created_at
                            q = o+timedelta(hours=5,minutes=30)
                            s = q.time()
                            a = str(s).split('.')
                            fredy = a[0]
                        else:
                            fredy = 'N/A'
                        disp = OrderTracking.objects.filter(Q(order_id=i.id),\
                                        Q(Order_staus_name_id=4))
                        if disp.count() > 0:
                            o = disp[0].created_at
                            q = o+timedelta(hours=5,minutes=30)
                            s = q.time()
                            a = str(s).split('.')
                            dredy = a[0]
                        else:
                            dredy = 'N/A'
                        delivered = OrderTracking.objects.filter(Q(order_id=i.id),\
                                        Q(Order_staus_name_id=5))
                        if delivered.count() > 0:
                            o = delivered[0].created_at
                            q = o+timedelta(hours=5,minutes=30)
                            s = q.time()
                            a = str(s).split('.')
                            delivered_time = a[0]
                            d_time     = o+timedelta(hours=5,minutes=30)
                            dtime = str(d_time.strftime("%I:%M %p"))
                            p_list['dispatch_time'] = dtime
                        else:
                            delivered_time = 'N/A'
                            p_list['dispatch_time'] = ''
                        # if disp.count() > 0 and delivered.count() > 0:
                        #     date_format = "%H:%M:%S"
                        #     t1 = datetime.strptime(str(dredy),date_format)
                        #     t2 = datetime.strptime(str(delivered_time),date_format)
                        #     f = t2 - t1
                        #     sec = f.total_seconds()
                        #     ddiff = f
                        #     p_list['delivered_time'] = ddiff
                        # else:
                        #     p_list['delivered_time'] = 'N/A'
                        ord_data.append(p_list)
                for obj in ord_data:
                    row_num += 1
                    o_time = obj['order_time']+timedelta(hours=5,minutes=30)
                    order_time = str(o_time.strftime("%I:%M %p"))
                    order_date = str(o_time.strftime("%d/%b/%y"))
                    row = [
                        order_date,
                        order_time,
                        obj['outlet_order_id'],
                        obj['outlet_name'],
                        obj['name'],
                        obj['mobile'],
                        obj['dispatch_time'],
                        obj['distance'],
                        obj['distance'],
                        obj['compensation'],
                        obj['amount']
                    ]
                    for col_num in range(len(row)):
                        ws.write(row_num, col_num, row[col_num], font_style)
                wb.save(response)
                return response
            else:
                pass


            if report_type == 'outlet':
                data = Order.objects.filter(Q(order_time__lte=end_date),Q(order_time__gte=start_date)
                        ,Q(Company_id=cid),Q(is_rider_assign=1))
                import xlwt
                response = HttpResponse(content_type='application/ms-excel')
                response['Content-Disposition'] = 'attachment; filename=rider_reports.xls'
                wb = xlwt.Workbook(encoding='utf-8')
                ws = wb.add_sheet("rider_reports")
                ws.write(0, 0, 'Start Date',xlwt.easyxf('align:horiz centre; pattern: pattern solid, fore_color orange;  font: color white,bold on,height 200'))
                ws.write(0, 1, s_date)
                ws.write(0, 2, 'End Date',xlwt.easyxf('align:horiz centre; pattern: pattern solid, fore_color orange;  font: color white,bold on,height 200'))
                ws.write(0, 3, e_date)
                font_style = xlwt.XFStyle()
                font_style.font.bold = True
                pattern = xlwt.Pattern()
                pattern.pattern = xlwt.Pattern.SOLID_PATTERN
                pattern.pattern_fore_colour = xlwt.Style.colour_map['blue']  # Set the cell background color to yellow
                font_style.pattern = pattern
                font_style = xlwt.XFStyle()
                font_style.alignment.wrap = 1
                date_format = xlwt.XFStyle()
                date_format.num_format_str = 'dd/mm/yyyy'

                row_num = 2
                columns = [
                    ("Order Date", 4000),
                    ("Order Time", 4000),
                    ("Order ID", 7000),
                    ("Outlet Name", 4000),
                    ("Rider Name", 4000),
                    ("Rider Mobile", 4000),
                    ("Dispatch Time", 3000),
                    ("Predicted KM", 12000),
                    ("Entered KM", 4000),
                    ("Compensation Rate", 5000),
                    ("Total Amount", 4000),
                  ]
                font_style = xlwt.XFStyle()
                font_style.font.bold = True
                for col_num in range(len(columns)):
                    ws.write(row_num, col_num, columns[col_num][0], font_style)
                    ws.col(col_num).width = columns[col_num][1]
                font_style = xlwt.XFStyle()
                font_style.alignment.wrap = 1
                ord_data =[]  
                tprice = 0
                if data.count() > 0:
                    for i in data:
                        p_list = {}
                        p_list['order_time'] = i.order_time
                        p_list['outlet_order_id'] = i.outlet_order_id
                        p_list['amount'] = i.total_bill_value
                        p_list['distance'] = i.distance
                        outlet_id = i.outlet_id
                        if outlet_id !=None:
                            p_list['outlet_name'] = OutletProfile.objects.filter(id=outlet_id)[0].Outletname
                        else:
                             p_list['outlet_name'] = 'N/A'
                        rider_data = ManagerProfile.objects.filter(id=i.delivery_boy_id)
                        if rider_data.count() > 0:
                            p_list['name']   = rider_data[0].manager_name + '' + rider_data[0].last_name
                            p_list['mobile'] = rider_data[0].mobile
                            p_list['compensation'] = rider_data[0].compensation
                            p_list['km'] = rider_data[0].km
                        else:
                            p_list['name'] = ''
                            p_list['mobile'] = ''
                            p_list['compensation'] = ''
                            p_list['km'] = ''
                        track_order = OrderTracking.objects.filter(Q(order_id=i.id),\
                                        Q(Order_staus_name_id=1))
                        if track_order.count() > 0:
                            o = track_order[0].created_at
                            q = o+timedelta(hours=5,minutes=30)
                            s = q.time()
                            a = str(s).split('.')
                            frd = a[0]
                        else:
                            frd = 'N/A'
                        atimes = OrderTracking.objects.filter(Q(order_id=i.id),\
                                        Q(Order_staus_name_id=2))
                        if atimes.count() > 0:
                            o = atimes[0].created_at
                            q = o+timedelta(hours=5,minutes=30)
                            s = q.time()
                            a = str(s).split('.')
                            act = a[0]
                        else:
                            act = 'N/A'
                        fready = OrderTracking.objects.filter(Q(order_id=i.id),\
                                        Q(Order_staus_name_id=3))
                        if fready.count() > 0:
                            o = fready[0].created_at
                            q = o+timedelta(hours=5,minutes=30)
                            s = q.time()
                            a = str(s).split('.')
                            fredy = a[0]
                        else:
                            fredy = 'N/A'
                        disp = OrderTracking.objects.filter(Q(order_id=i.id),\
                                        Q(Order_staus_name_id=4))
                        if disp.count() > 0:
                            o = disp[0].created_at
                            q = o+timedelta(hours=5,minutes=30)
                            s = q.time()
                            a = str(s).split('.')
                            dredy = a[0]
                        else:
                            dredy = 'N/A'
                        delivered = OrderTracking.objects.filter(Q(order_id=i.id),\
                                        Q(Order_staus_name_id=5))
                        if delivered.count() > 0:
                            o = delivered[0].created_at
                            q = o+timedelta(hours=5,minutes=30)
                            s = q.time()
                            a = str(s).split('.')
                            delivered_time = a[0]
                            d_time     = o+timedelta(hours=5,minutes=30)
                            dtime = str(d_time.strftime("%I:%M %p"))
                            p_list['dispatch_time'] = dtime
                        else:
                            delivered_time = 'N/A'
                            p_list['dispatch_time'] = ''
                        # if disp.count() > 0 and delivered.count() > 0:
                        #     date_format = "%H:%M:%S"
                        #     t1 = datetime.strptime(str(dredy),date_format)
                        #     t2 = datetime.strptime(str(delivered_time),date_format)
                        #     f = t2 - t1
                        #     sec = f.total_seconds()
                        #     ddiff = f
                        #     p_list['delivered_time'] = ddiff
                        # else:
                        #     p_list['delivered_time'] = 'N/A'
                        ord_data.append(p_list)
                for obj in ord_data:
                    row_num += 1
                    o_time = obj['order_time']+timedelta(hours=5,minutes=30)
                    order_time = str(o_time.strftime("%I:%M %p"))
                    order_date = str(o_time.strftime("%d/%b/%y"))
                    row = [
                        order_date,
                        order_time,
                        obj['outlet_order_id'],
                        obj['outlet_name'],
                        obj['name'],
                        obj['mobile'],
                        obj['dispatch_time'],
                        obj['distance'],
                        obj['distance'],
                        obj['compensation'],
                        obj['amount']
                    ]
                    for col_num in range(len(row)):
                        ws.write(row_num, col_num, row[col_num], font_style)
                wb.save(response)
                return response
            else:
                pass


class Riderlist(APIView):
    """
    Rider listing and searching  POST API

        Authentication Required     : Yes
        Service Usage & Description : This Api is used for Order listng and searcing of Brand.

        Data Post: {
            "start_date"            : "2019-07-24 00:00:00:00",
            "end_date"              : "2019-07-29 00:00:00:00"  
            "staff"                 :           
        }

        Response: {

            "success": True, 
            "data": final_result
        }

    """
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            mutable = request.POST._mutable
            request.POST._mutable = True
            data = request.data
            err_message = {}
            if data["start_date"] != '' and data["end_date"] != '':
                start_date = dateutil.parser.parse(data["start_date"])
                end_date = dateutil.parser.parse(data["end_date"])
                if start_date > end_date:
                    err_message["from_till"] = "Validity dates are not valid!!"
            else:
                pass
            if any(err_message.values())==True:
                return Response({
                    "success": False,
                    "error" : err_message,
                    "message" : "Please correct listed errors!!"
                    })
                
            user = request.user.id
            cid = get_user(user)
            final_result = []
            data = Order.objects.filter(Q(order_time__lte=end_date),Q(order_time__gte=start_date)
                        ,Q(Company_id=cid),Q(delivery_boy_id=data['rider']))
            if data.count() > 0:
                for i in data:
                    p_list = {}
                    o_time     = i.order_time+timedelta(hours=5,minutes=30)
                    order_time = str(o_time.strftime("%I:%M %p"))
                    order_date = str(o_time.strftime("%d/%b/%y"))
                    p_list['order_date'] = order_date
                    p_list['order_time'] = order_time
                    p_list['outlet_order_id'] = i.outlet_order_id
                    p_list['amount'] = i.total_bill_value
                    outlet_id = i.outlet_id
                    if outlet_id !=None:
                        p_list['outlet_name'] = OutletProfile.objects.filter(id=outlet_id)[0].Outletname
                    else:
                         p_list['outlet_name'] = 'N/A'
                    rider_data = ManagerProfile.objects.filter(id=i.delivery_boy_id)
                    if rider_data.count() > 0:
                        p_list['name'] = rider_data[0].manager_name + '' + rider_data[0].last_name
                        p_list['mobile'] = rider_data[0].mobile
                        p_list['compensation'] = rider_data[0].compensation
                        p_list['km'] = rider_data[0].km
                    else:
                        p_list['name'] = ''
                        p_list['mobile'] = ''
                        p_list['compensation'] = ''
                        p_list['km'] = ''
                    track_order = OrderTracking.objects.filter(Q(order_id=i.id),\
                                    Q(Order_staus_name_id=1))
                    if track_order.count() > 0:
                        o = track_order[0].created_at
                        q = o+timedelta(hours=5,minutes=30)
                        s = q.time()
                        a = str(s).split('.')
                        frd = a[0]
                    else:
                        frd = 'N/A'
                    atimes = OrderTracking.objects.filter(Q(order_id=i.id),\
                                    Q(Order_staus_name_id=2))
                    if atimes.count() > 0:
                        o = atimes[0].created_at
                        q = o+timedelta(hours=5,minutes=30)
                        s = q.time()
                        a = str(s).split('.')
                        act = a[0]
                    else:
                        act = 'N/A'
                    fready = OrderTracking.objects.filter(Q(order_id=i.id),\
                                    Q(Order_staus_name_id=3))
                    if fready.count() > 0:
                        o = fready[0].created_at
                        q = o+timedelta(hours=5,minutes=30)
                        s = q.time()
                        a = str(s).split('.')
                        fredy = a[0]
                    else:
                        fredy = 'N/A'
                    disp = OrderTracking.objects.filter(Q(order_id=i.id),\
                                    Q(Order_staus_name_id=4))
                    if disp.count() > 0:
                        o = disp[0].created_at
                        q = o+timedelta(hours=5,minutes=30)
                        s = q.time()
                        a = str(s).split('.')
                        dredy = a[0]
                    else:
                        dredy = 'N/A'
                    delivered = OrderTracking.objects.filter(Q(order_id=i.id),\
                                    Q(Order_staus_name_id=5))
                    if delivered.count() > 0:
                        o = delivered[0].created_at
                        q = o+timedelta(hours=5,minutes=30)
                        s = q.time()
                        a = str(s).split('.')
                        delivered_time = a[0]
                        d_time     = o+timedelta(hours=5,minutes=30)
                        dtime = str(d_time.strftime("%I:%M %p"))
                        p_list['delivered_time'] = dtime
                    else:
                        delivered_time = 'N/A'
                    if disp.count() > 0 and delivered.count() > 0:
                        date_format = "%H:%M:%S"
                        t1 = datetime.strptime(str(dredy),date_format)
                        t2 = datetime.strptime(str(delivered_time),date_format)
                        f = t2 - t1
                        sec = f.total_seconds()
                        ddiff = f
                        p_list['dispatch_time'] = s
                    else:
                        p_list['delivered_time'] = 'N/A'
                    final_result.append(p_list)
            else:
                pass
            return Response({"status":True,
                             "data" : final_result})
        except Exception as e:
            print(e)
            return Response(
                        {"error":str(e)}
                        )
            










