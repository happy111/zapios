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

def convert(seconds): 
    seconds = seconds % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d:%02d:%02d" % (hour, minutes, seconds) 



class OutletPerformance(APIView):
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
            st = request.GET.get('outlet')
            outletss = list(st.split(",")) 
            day = request.GET.get('days')
            if day == None or day == '' or day  == 'undefined':
                day = 'Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday'
                allday = list(day.split(",")) 
            else:
                allday = list(day.split(",")) 
            import xlwt
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename=outlet_performance.xls'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet("OutletPerformance_reports")
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
                ("Outlet Name", 4000),
                ("Day", 4000),
                ("Number Of Order", 4000),
                ("7 To 11", 2000),
                ("11 To 3", 2000),
                ("3 To 6", 2000),
                ("6 To 9", 2000),
                ("9 To 12", 2000),
                ("Average Food Prep Time", 6000),
                ("Average Time for Packing", 6000),
                ("Average Time to Dispatch", 6000),
                ("Average time to Settle Order", 6000),
              ]
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num][0], font_style)
                ws.col(col_num).width = columns[col_num][1]
            font_style = xlwt.XFStyle()
            font_style.alignment.wrap = 1
            tprice = 0
            start_date = dateutil.parser.parse(s_date)
            next_data = start_date+timedelta(1)
            dday= (end_date - start_date).days
            ord_data = []



            for i in range(1,dday+2):
                for day in allday:
                    order_data = Order.objects.filter(Q(order_time__date=start_date),Q(Company_id=cid),\
                        Q(day=day))
                    if order_data.count() > 0:
                        for outlet in outletss:
                            data = order_data.filter(outlet_id=outlet)
                            if data.count() > 0:
                                p_list = {}
                                p_list['total_order'] = data.count()
                                p_list['day']         = data[0].order_time.strftime('%A')
                                p_list['order_date']  = data[0].order_time
                                p_list['outlet_name'] = OutletProfile.objects.filter(id=outlet)[0].Outletname
                                seven = 0
                                eleven = 0
                                three = 0
                                six = 0
                                nine = 0
                                food_second = 0
                                dis_second = 0
                                settle_second = 0
                                food_time = 0
                                diff = 0
                                diff1 = 0
                                for index in data:
                                    order_time            = index.order_time+timedelta(hours=5,minutes=30)
                                    order_time = index.order_time+timedelta(hours=5,minutes=30)
                                    hour = order_time.hour
                                    if hour >= 7 and hour <=11:
                                        seven = seven + 1
                                        p_list['seven'] = seven
                                    else:
                                         p_list['seven'] = seven
                                    if hour > 11 and hour <=15:
                                        eleven = eleven + 1
                                        p_list['eleven'] = eleven
                                    else:
                                         p_list['eleven'] = eleven
                                    if hour > 15 and hour <=18:
                                        three = three + 1
                                        p_list['three'] = three
                                    else:
                                         p_list['three'] = three
                                    if hour > 18 and hour <=21:
                                        six = six + 1
                                        p_list['six'] = six
                                    else:
                                         p_list['six'] = six
                                    if hour > 21 and hour <=24:
                                        nine = nine + 1
                                        p_list['nine'] = nine
                                    else:
                                         p_list['nine'] = nine
                                
                                    track_order = OrderTracking.objects.filter(Q(order_id=index.id),\
                                                    Q(Order_staus_name_id=2))
                                    if track_order.count() > 0:
                                        o = track_order[0].created_at
                                        q = o+timedelta(hours=5,minutes=30)
                                        s = q.time()
                                        a = str(s).split('.')
                                        frd = a[0]
                                    else:
                                        frd = 'N/A'
                                    atimes = OrderTracking.objects.filter(Q(order_id=index.id),\
                                                    Q(Order_staus_name_id=3))
                                    if atimes.count() > 0:
                                        o = atimes[0].created_at
                                        q = o+timedelta(hours=5,minutes=30)
                                        s = q.time()
                                        a = str(s).split('.')
                                        act = a[0]
                                    else:
                                        act = 'N/A'
                                    disp = OrderTracking.objects.filter(Q(order_id=index.id),\
                                                    Q(Order_staus_name_id=4))
                                    if disp.count() > 0:
                                        o = disp[0].created_at
                                        q = o+timedelta(hours=5,minutes=30)
                                        s = q.time()
                                        a = str(s).split('.')
                                        dredy = a[0]
                                    else:
                                        dredy = 'N/A'
                                    settle = OrderTracking.objects.filter(Q(order_id=index.id),\
                                                    Q(Order_staus_name_id=6))
                                    if settle.count() > 0:
                                        o = settle[0].created_at
                                        q = o+timedelta(hours=5,minutes=30)
                                        s = q.time()
                                        a = str(s).split('.')
                                        settle_time = a[0]
                                    else:
                                        settle_time = 'N/A'
                                    if track_order.count() > 0 and atimes.count() > 0:
                                        date_format = "%H:%M:%S"
                                        t1 = datetime.strptime(str(frd),date_format)
                                        t2 = datetime.strptime(str(act),date_format)
                                        dif = t2 - t1
                                        sec = dif.total_seconds()
                                        diff = dif
                                    else:
                                        pass

                                    if diff != 0:
                                        food_second = food_second + sec
                                        average_sec = food_second // data.count()
                                        f_average_sec = convert(average_sec)
                                        p_list['average_food_ready'] = f_average_sec
                                    else:
                                        p_list['average_food_ready'] = 0
                                    if track_order.count() > 0 and disp.count() > 0:
                                        date_format = "%H:%M:%S"
                                        t1 = datetime.strptime(str(frd),date_format)
                                        t2 = datetime.strptime(str(dredy),date_format)
                                        dif = t2 - t1
                                        sec1 = dif.total_seconds()
                                        diff1 = dif
                                    else:
                                        pass
                                    if diff1 != 0:
                                        dis_second = dis_second + sec1
                                        average_sec = dis_second // data.count()
                                        d_average_sec = convert(average_sec)
                                        p_list['average_dispatch_ready'] = d_average_sec
                                    else:
                                        p_list['average_dispatch_ready'] = 0
                                    if track_order.count() > 0 and settle.count() > 0:
                                        date_format = "%H:%M:%S"
                                        t1 = datetime.strptime(str(frd),date_format)
                                        t2 = datetime.strptime(str(settle_time),date_format)
                                        dif = t2 - t1
                                        sec2 = dif.total_seconds()
                                        diff2 = dif
                                    else:
                                        diff2 = 'N/A'
                                        sec2 = 0
                                    if diff2 != str:
                                        settle_second = settle_second + sec2
                                        average_sec = settle_second // data.count()
                                        s_average_sec = convert(average_sec)
                                        p_list['average_settle_ready'] = s_average_sec
                                    else:
                                         p_list['average_settle_ready'] = ''
                                    if atimes.count() > 0 and disp.count() > 0:
                                        date_format = "%H:%M:%S"
                                        t1 = datetime.strptime(str(act),date_format)
                                        t2 = datetime.strptime(str(dredy),date_format)
                                        dif = t2 - t1
                                        sec3 = dif.total_seconds()
                                        diff3 = dif
                                    else:
                                        diff3 = 'N/A'
                                        sec3 = 0
                                    if diff3 != str:
                                        food_time = food_time + sec3
                                        average_sec = food_time // data.count()
                                        s_average_sec = convert(average_sec)
                                        p_list['food_time'] = s_average_sec
                                    else:
                                         p_list['food_time'] = ''
                                ord_data.append(p_list)
                start_date = start_date+timedelta(1)
            if len(ord_data) > 0:
                for obj in ord_data:
                    row_num += 1
                    o_time = obj['order_date']+timedelta(hours=5,minutes=30)
                    order_time = str(o_time.strftime("%I:%M %p"))
                    order_date = str(o_time.strftime("%d/%b/%y"))
                    row = [
                        order_date,
                        obj['outlet_name'],
                        obj['day'],
                        obj['total_order'],
                        obj['seven'],
                        obj['eleven'],
                        obj['three'],
                        obj['six'],
                        obj['nine'],
                        obj['average_food_ready'],
                        obj['food_time'],
                        obj['average_dispatch_ready'],
                        obj['average_settle_ready']
                    ]
                    for col_num in range(len(row)):
                        ws.write(row_num, col_num, row[col_num], font_style)
                wb.save(response)
                return response
            else:
                wb.save(response)
                return response




