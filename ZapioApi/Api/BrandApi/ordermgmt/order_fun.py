from rest_framework.views import APIView
from rest_framework.response import Response
from ZapioApi.api_packages import *
from datetime import datetime, timedelta
from Orders.models import Order, OrderStatusType, OrderTracking
from Product.models import *
from Outlet.Api.serializers.order_serializers import (
    BoySerializer,
    OrderTrackSerializer,
    OrderSerializer,
)
from Outlet.models import DeliveryBoy, OutletProfile
from UserRole.models import *
from Brands.models import Company
from Configuration.models import OrderSource
from Configuration.models import DeliverySetting,ProductWeightage,TaxSetting
from zapio.settings import Media_Path



li = ["Acknowledged", "Food Ready", "Dispatched", "Completed", "Cancelled"]


def urban_order(order_data):
    urban_order_id = order_data.urban_order_id
    urban_record = UrbanOrders.objects.filter(order_id=urban_order_id)
    if urban_record.count() == 0:
        return False
    else:
        q = urban_record[0]
        next_states = q.next_states
        current_state = q.order_state
        if current_state == "Food Ready":
            return "cannot_process"
        else:
            pass
        if current_state not in next_states:
            status_change = next_states[0]
        elif (
            current_state != "Dispatched"
            and current_state != "Completed"
            and current_state != "Cancelled"
        ):
            status_change = "Food Ready"
        else:
            return "cannot_process"
        sync_order = Order_status_update(urban_order_id, status_change)
        # else:
        # 	return "cannot_process"
        if sync_order == None:
            return False
        else:
            return "processed"


def ChangestatusData(data):
    uid = data["user"]
    user_data = ManagerProfile.objects.filter(auth_user_id=uid)
    key_person = user_data[0].username
    err_message = {}
    order_track = {}
    dboy = {}
    order_dict = {}
    err_message["order_id"] = validation_master_anything(
        data["order_id"], "Order Id", contact_re, 1
    )
    if any(err_message.values()) == True:
        err = {
            "success": False,
            "error": err_message,
            "message": "Please correct listed errors!!",
        }
        return err
    order_record = Order.objects.filter(id=data["order_id"])
    order_data = order_record.first()
    urban_order_id = order_data.urban_order_id
    if order_data.is_aggregator == True:
        urban_process = urban_order(order_data)
        if urban_process == False:
            err = {
                "success": False,
                "message": "Order can'nt be processed..something went wrong while"
                " communicating with third party services!!",
            }
            return err
        elif urban_process == "cannot_process":
            err = {"success": False, "message": "Order is already processed!!"}
            return err
        else:
            pass
    else:
        pass
    updated_order = Order.objects.filter(urban_order_id=urban_order_id)
    Aggregator_order_status = updated_order[0].Aggregator_order_status
    order_status_id = order_data.order_status.id
    order_priority = order_data.order_status.priority
    order_status_record = OrderStatusType.objects.filter(
        id__gt=order_status_id, priority__gt=order_priority, active_status=1
    ).order_by("priority")
    if order_status_record.count() == 0:
        err_message = {}
        err_message["change_status"] = "Order is already processed!!"
        err = {"error": err_message, "message": "Please correct listed errors!!"}
        return err
    else:
        if order_data.is_aggregator == False:
            order_dict["order_status"] = order_status_record[0].id
            is_delivered_rec = OrderStatusType.objects.filter(
                id=order_dict["order_status"]
            )
            if is_delivered_rec[0].Order_staus_name == "Delivered":
                order_dict["delivery_time"] = datetime.now()
                order_dict["is_completed"] = 1
            else:
                pass
            order_dict["Aggregator_order_status"] = Aggregator_order_status
            a = ManagerProfile.objects.filter(auth_user_id=data["user"])
            order_dict["user"] = a[0].username
            Order_serializer = OrderSerializer(
                order_data, data=order_dict, partial=True
            )
            if Order_serializer.is_valid():
                s = Order_serializer.save()
                order_track["order"] = data["order_id"]
                order_track["Order_staus_name"] = order_dict["order_status"]
                if order_track['Order_staus_name'] == 7:
                    order_track["Order_staus_name"] = 6
                order_track["key_person"] = key_person
                Order_track_serializer = OrderTrackSerializer(data=order_track)
                if Order_track_serializer.is_valid():
                    Order_track_serializer.save()
                else:
                    err = {
                        "success": False,
                        "message": Order_track_serializer.errors,
                    }
                    return err
            else:
                err = {
                    "success": False,
                    "message": Order_serializer.errors,
                }
            err = {
                "success": True,
                "message": "Order Status changed successfully!!",
            }
        else:
            err = {
                "success": True,
                "message": "Order Status changed successfully!!",
            }
        return err


def RetrievalData(data):
    if 'id' in data:
        data["id"] = str(data["id"])
        err_message = {}
        err_message["id"] = validation_master_anything(
            data["id"], "Order Id", contact_re, 1
        )
        if any(err_message.values()) == True:
            err = {
                "success": False,
                "error": err_message,
                "message": "Please correct listed errors!!",
            }
            return err
        order_record = Order.objects.filter(id=data["id"])
        if order_record.count() == 0:
            err = {
                "success": False,
                "message": "Required Order data is not valid to retrieve!!",
            }
            return err
        else:
            final_result = []
            p_list = {}
            p_list["id"] = order_record[0].id
            add = order_record[0].address
            p_list["order_id"] = order_record[0].order_id
            p_list["log"] = []
            orderlog = OrderTracking.objects.filter(order_id=p_list["id"]).order_by("id")
            if orderlog.count() > 0:
                for j in orderlog:
                    r_list = {}
                    r_list["id"] = j.id
                    r_list["status_name"] = j.Order_staus_name.Order_staus_name
                    created_at = j.created_at + timedelta(hours=5, minutes=30)
                    r_list["created_at"] = created_at.isoformat()
                    r_list["key_person"] = j.key_person
                    p_list["log"].append(r_list)
            else:
                pass
            p_list["order_status"] = order_record[0].order_status_id
            p_list["source"] = order_record[0].order_source.source_name
            full_path = addr_set()
            if (
                order_record[0].order_source.image != None
                and order_record[0].order_source.image != ""
            ):
                p_list["pic"] = full_path + str(order_record[0].order_source.image)
            else:
                p_list["pic"] = ""
            if order_record[0].settlement_details != None:
                if len(order_record[0].settlement_details) > 0:
                    p_list["payment_mode"] = []
                    for k in order_record[0].settlement_details:
                        if k["mode"] != None:
                            mode = {}
                            mode["pmode"] = k["payment_name"]
                            p_list["payment_mode"].append(mode["pmode"])
                        else:
                            if order_record[0].is_aggregator == True:
                                p_list["payment_mode"] = order_record[
                                    0
                                ].aggregator_payment_mode
                            else:
                                p_list["payment_mode"] = ""
                else:
                    if order_record[0].order_source.source_name == 'Website Order':
                        p_list["payment_mode"] = order_record[0].payment_mode
                    else:
                        p_list["payment_mode"] = ""
            else:
                if order_record[0].order_source.source_name == 'Website Order':
                    p_list["payment_mode"] = order_record[0].payment_mode
                else:
                    if order_record[0].is_aggregator == True:
                        p_list["payment_mode"] = order_record[0].aggregator_payment_mode
                    else:
                        p_list["payment_mode"] = ""
            if order_record[0].is_aggregator == False:
                p_list["order_status_name"] = (
                    OrderStatusType.objects.filter(id=order_record[0].order_status_id)
                    .first()
                    .Order_staus_name
                )
                p_list["color_code"] = (
                    OrderStatusType.objects.filter(id=order_record[0].order_status_id)
                    .first()
                    .color_code
                )
            else:
                p_list["order_status_name"] = order_record[0].Aggregator_order_status
            cus = order_record[0].customer
            if cus != "":
                p_list["first_name"] = cus["first_name"]
                p_list["last_name"]  = cus["last_name"]
                if "email" in cus:
                    p_list["email"] = cus["email"]
                else:
                    pass
                if "mobile_number" in cus:
                    p_list["mobile"] = cus["mobile_number"]

                if "mobile" in cus:
                    p_list["mobile"] = cus["mobile"]
            else:
                pass
            p_list["order_description"] = order_record[0].order_description
            p_list["qty"] = len(order_record[0].order_description)
            tt = order_record[0].tax_detail
            alltax = TaxSetting.objects.filter(company=order_record[0].Company_id)
            p_list["tax_detail"] = []
            o_time = order_record[0].order_time + timedelta(hours=5, minutes=30)
            p_list["order_time"] = o_time.isoformat()
            if order_record[0].delivery_time != None:
                d_time = order_record[0].delivery_time + timedelta(hours=5, minutes=30)
                p_list["delivery_time"] = d_time.isoformat()
            else:
                p_list["delivery_time"] = None
            p_list["taxes"] = order_record[0].taxes
            p_list["sub_total"] = order_record[0].sub_total
            p_list["total_bill_value"] = order_record[0].total_bill_value
            p_list["special_instructions"] = order_record[0].special_instructions
            p_list["is_rider_assign"] = order_record[0].is_rider_assign
            p_list["other_order_id"] = order_record[0].outlet_order_id
            p_list["channel_order_id"] = order_record[0].channel_order_id
            p_list["cancel_reason"] = order_record[0].order_cancel_reason
            p_list["delivery_instructions"] = order_record[0].delivery_instructions
            p_list["cancel_responsibility"] = order_record[0].cancel_responsibility
            p_list["delivery_charge"] = order_record[0].delivery_charge
            p_list["packing_charge"] = order_record[0].packing_charge
            p_list["rider_id"] = order_record[0].delivery_boy_id
            p_list["discount_name"]  = order_record[0].discount_name
            p_list["discount_value"] = order_record[0].discount_value
            p_list["coupon_code"] = order_record[0].coupon_code
            if p_list['coupon_code']:
                if 'discount' in order_record[0].order_description[0]:
                    p_list["discount_value"] =order_record[0].order_description[0]['discount']
                p_list["discount_name"] = order_record[0].coupon_code
            p_list["rider_detail"] = []
            if order_record[0].is_rider_assign == True:
                if order_record[0].is_aggregator == False:
                    a = {}
                    ad = ManagerProfile.objects.filter(id=order_record[0].delivery_boy_id)
                    a["name"] = ad[0].manager_name
                    a["email"] = ad[0].email
                    a["mobile"] = ad[0].mobile
                    p_list["rider_detail"].append(a)
                else:
                    rider_detail = order_record[0].delivery_boy_details
                    p_list["rider_detail"].append(rider_detail)
            else:
                a = {}
                a["name"] = ""
                a["email"] = ""
                a["mobile"] = ""
                p_list["rider_detail"].append(a)
            p_list["address"] = []
           
            if len(order_record[0].address) > 0:
                for index in order_record[0].address:
                    dic = {}
                    if 'city' in index:
                        try:
                            city = int(index["city"])
                            city_data = CityMaster.objects.filter(id=index['city'])
                            if city_data.count() > 0:
                                dic['city'] = city_data[0].city
                            else:
                                dic['city'] = index['city']
                        except Exception as e:
                            dic['city'] = index['city']
                    if 'locality' in index:
                        try:
                            locality = int(index["locality"])
                            city_data = CityMaster.objects.filter(id=index['city'])
                            locality_data = AreaMaster.objects.filter(id=index['locality'])
                            if locality_data.count() > 0:
                                dic['locality'] = locality_data[0].area
                            else:
                                dic['locality'] = index['locality']
                        except Exception as e:
                            dic['locality'] = index['locality']
                    if 'address' in index:
                        dic['address'] = index['address']
                    else:
                        dic['address'] = ''
                    if 'address_type' in index:
                        dic['address_type'] = index['address_type']
                    else:
                        dic['address_type'] = ''
                    p_list['address'].append(dic)
            final_result.append(p_list)
            err = {
                "success": True,
                "message": "Order data retrieval api worked well!!",
                "data": final_result,
            }
        return err
    else:
        return


def get_user(user):
    is_brand = Company.objects.filter(auth_user=user)
    is_cashier = ManagerProfile.objects.filter(auth_user_id=user)
    if is_cashier.count() > 0:
        cid = ManagerProfile.objects.filter(auth_user_id=user)[0].Company_id
    else:
        pass
    if is_brand.count() > 0:
        print("Love")
        outlet = Company.objects.filter(auth_user_id=user)
        cid = outlet[0].id
    else:
        pass
    return cid


def ProductStatus(id,cid):
    productData = Product.objects.filter(id=id)[0]
    data = ProductWeightage.objects.filter(company_id=cid)
    if data.count() > 0:
        dataweight = ProductWeightage.objects.filter(company_id=cid)[0]
        totalstatus = 0
        imgdata = ProductImage.objects.filter(product_id=id)
        if(len(productData.product_categorys)) > 0:
            totalstatus = totalstatus + int(dataweight.product_category)
        else:
            totalstatus = totalstatus + 0
        if(len(productData.product_subcategorys)) > 0:
            totalstatus = totalstatus + int(dataweight.product_subcategory)
        else:
            totalstatus = totalstatus + 0
        if productData.product_name !=None:
            totalstatus = totalstatus + int(dataweight.product_name)
        else:
            totalstatus = totalstatus + 0
        if productData.food_type !=None:
            totalstatus = totalstatus + int(dataweight.food_type)
        else:
            totalstatus = totalstatus + 0
        if productData.priority !=None:
            totalstatus = totalstatus + int(dataweight.priority)
        else:
            totalstatus = totalstatus + 0
        if productData.product_code !=None:
            totalstatus = totalstatus + int(dataweight.product_code)
        else:
            totalstatus = totalstatus + 0
        if productData.product_desc !=None:
            totalstatus = totalstatus + int(dataweight.product_desc)
        else:
            totalstatus = totalstatus + 0
        if productData.allergen_Information !=None:
            totalstatus = totalstatus + int(dataweight.allergen_Information)
        else:
            totalstatus = totalstatus + 0
        if productData.spice !=None:
            totalstatus = totalstatus + int(dataweight.spice)
        else:
            totalstatus = totalstatus + 0
        if productData.kot_desc !=None:
            totalstatus = totalstatus + int(dataweight.kot_desc)
        else:
            totalstatus = totalstatus + 0
        if productData.pvideo !=None:
            totalstatus = totalstatus + int(dataweight.pvideo)
        else:
            totalstatus = totalstatus + 0
        if imgdata.count() > 0:
            totalstatus = totalstatus + int(dataweight.product_image)
        else:
            totalstatus = totalstatus + 0
        if productData.tags !=None:
            totalstatus = totalstatus + int(dataweight.tags)
        else:
            totalstatus = totalstatus + 0
        if productData.price !=None:
            totalstatus = totalstatus + int(dataweight.price)
        else:
            totalstatus = totalstatus + 0
        if productData.discount_price !=None:
            totalstatus = totalstatus + int(dataweight.discount_price)
        else:
            totalstatus = totalstatus + 0
        if productData.variant_deatils !=None:
            totalstatus = totalstatus + int(dataweight.variant_deatils)
        else:
            totalstatus = totalstatus + 0
        if productData.addpn_grp_association !=None:
            totalstatus = totalstatus + int(dataweight.addpn_grp_association)
        else:
            totalstatus = totalstatus + 0

        if productData.tax_association != None:
            totalstatus = totalstatus + int(dataweight.tax_association)
        else:
            totalstatus = totalstatus + 0
        if productData.product_schema != None:
            if(len(productData.product_schema)) > 0:
                totalstatus = totalstatus + int(dataweight.product_schema)
            else:
                totalstatus = totalstatus + 0
        else:
            totalstatus = totalstatus + 0
        return totalstatus
    else:
        return 0



def Changestatus(data):
    uid = data["user"]
    user_data = ManagerProfile.objects.filter(auth_user_id=uid)
    key_person = user_data[0].username
    err_message = {}
    order_track = {}
    dboy = {}
    order_dict = {}
    err_message["order_id"] = validation_master_anything(
        data["order_id"], "Order Id", contact_re, 1
    )
    if any(err_message.values()) == True:
        err = {
            "success": False,
            "error": err_message,
            "message": "Please correct listed errors!!",
        }
        return err
    order_record = Order.objects.filter(id=data["order_id"])
    order_data = order_record.first()
    urban_order_id = order_data.urban_order_id


    if order_data.is_aggregator == True:
        urban_process = urban_order(order_data)
        if urban_process == False:
            err = {
                "success": False,
                "message": "Order can'nt be processed..something went wrong while"
                " communicating with third party services!!",
            }
            return err
        elif urban_process == "cannot_process":
            err = {"success": False, "message": "Order is already processed!!"}
            return err
        else:
            pass
    else:
        pass
    updated_order = Order.objects.filter(urban_order_id=urban_order_id)
    Aggregator_order_status = updated_order[0].Aggregator_order_status
    order_status_id = order_data.order_status.id
    order_priority = order_data.order_status.priority
    order_status_record = OrderStatusType.objects.filter(
        id__gt=order_status_id, priority__gt=order_priority, active_status=1
    ).order_by("priority")
    if order_status_record.count() == 0:
        err_message = {}
        err_message["change_status"] = "Order is already processed!!"
        err = {"error": err_message, "message": "Please correct listed errors!!"}
        return err
    else:
        if order_data.is_aggregator == False:
            order_dict["order_status"] = order_status_record[0].id
            is_delivered_rec = OrderStatusType.objects.filter(
                id=order_dict["order_status"]
            )
            if is_delivered_rec[0].Order_staus_name == "Delivered":
                order_dict["delivery_time"] = datetime.now()
                order_dict["is_completed"] = 1
            else:
                pass
            order_dict["Aggregator_order_status"] = Aggregator_order_status
            a = ManagerProfile.objects.filter(auth_user_id=data["user"])
            order_dict["user"] = a[0].username
            Order_serializer = OrderSerializer(
                order_data, data=order_dict, partial=True
            )
            if Order_serializer.is_valid():
                s = Order_serializer.save()
                order_track["order"] = data["order_id"]
                order_track["Order_staus_name"] = order_dict["order_status"]
                order_track["key_person"] = key_person
                Order_track_serializer = OrderTrackSerializer(data=order_track)
                if Order_track_serializer.is_valid():
                    Order_track_serializer.save()
                else:
                    err = {
                        "success": False,
                        "message": Order_track_serializer.errors,
                    }
                    return err
            else:
                err = {
                    "success": False,
                    "message": Order_serializer.errors,
                }
            err = {
                "success": True,
                "message": "Order Status changed successfully!!",
            }
        else:
            err = {
                "success": True,
                "message": "Order Status changed successfully!!",
            }
        return err



def RetrievalCMSData(data):
    data["id"] = str(data["id"])
    err_message = {}
    err_message["id"] = validation_master_anything(
        data["id"], "Order Id", contact_re, 1
    )
    if any(err_message.values()) == True:
        err = {
            "success": False,
            "error": err_message,
            "message": "Please correct listed errors!!",
        }
        return err
    order_record = Order.objects.filter(id=data["id"])
    if order_record.count() == 0:
        err = {
            "success": False,
            "message": "Required Order data is not valid to retrieve!!",
        }
        return err
    else:
        final_result = []
        p_list = {}
        p_list["id"] = order_record[0].id
        add = order_record[0].address
        p_list["order_id"] = order_record[0].order_id
        p_list["log"] = []
        orderlog = OrderTracking.objects.filter(order_id=p_list["id"]).order_by("id")
        if orderlog.count() > 0:
            for j in orderlog:
                r_list = {}
                r_list["id"] = j.id
                r_list["status_name"] = j.Order_staus_name.Order_staus_name
                created_at = j.created_at + timedelta(hours=5, minutes=30)
                r_list["created_at"] = created_at.isoformat()
                r_list["key_person"] = j.key_person
                p_list["log"].append(r_list)
        else:
            pass
        p_list["order_status"] = order_record[0].order_status_id
        p_list["source"] = order_record[0].order_source.source_name
        full_path = addr_set()
        if (
            order_record[0].order_source.image != None
            and order_record[0].order_source.image != ""
        ):
            p_list["pic"] = full_path + str(order_record[0].order_source.image)
        else:
            p_list["pic"] = ""
        if order_record[0].settlement_details != None:
            if len(order_record[0].settlement_details) > 0:
                p_list["payment_mode"] = []
                for k in order_record[0].settlement_details:
                    if k["mode"] != None:
                        mode = {}
                        mode["pmode"] = k["payment_name"]
                        p_list["payment_mode"].append(mode["pmode"])
                    else:
                        if order_record[0].is_aggregator == True:
                            p_list["payment_mode"] = order_record[
                                0
                            ].aggregator_payment_mode
                        else:
                            p_list["payment_mode"] = ""
            else:
                if order_record[0].order_source.source_name == 'Website Order':
                    p_list["payment_mode"] = order_record[0].payment_mode
                else:
                    p_list["payment_mode"] = ""
        else:
            if order_record[0].order_source.source_name == 'Website Order':
                p_list["payment_mode"] = order_record[0].payment_mode
            else:
                if order_record[0].is_aggregator == True:
                    p_list["payment_mode"] = order_record[0].aggregator_payment_mode
                else:
                    p_list["payment_mode"] = ""
        if order_record[0].is_aggregator == False:
            p_list["order_status_name"] = (
                OrderStatusType.objects.filter(id=order_record[0].order_status_id)
                .first()
                .Order_staus_name
            )
            p_list["color_code"] = (
                OrderStatusType.objects.filter(id=order_record[0].order_status_id)
                .first()
                .color_code
            )
        else:
            p_list["order_status_name"] = order_record[0].Aggregator_order_status
        cus = order_record[0].customer
        if cus != "":
            p_list["first_name"] = cus["first_name"]
            p_list["last_name"] = cus["last_name"]
            if "email" in cus:
                p_list["email"] = cus["email"]
            else:
                pass
            if "mobile_number" in cus:
                p_list["mobile"] = cus["mobile_number"]

            if "mobile" in cus:
                p_list["mobile"] = cus["mobile"]
        else:
            pass
        p_list["order_description"] = order_record[0].order_description
        if len(p_list['order_description']) > 0:
            for i in p_list['order_description']:
                chk_imag = ProductImage.objects.filter(product_id=i['id'],primary_image=1)
                if chk_imag.count() > 0:
                    i['image'] = Media_Path+str(chk_imag[0].product_image)
                else:
                    i['image'] = None
        p_list["qty"] = len(order_record[0].order_description)
        tt = order_record[0].tax_detail
        alltax = TaxSetting.objects.filter(company=order_record[0].Company_id)
        p_list["tax_detail"] = []
        o_time = order_record[0].order_time + timedelta(hours=5, minutes=30)
        p_list["order_time"] = o_time.strftime("%Y-%b-%d %I:%M %p")
        if order_record[0].delivery_time != None:
            d_time = order_record[0].delivery_time + timedelta(hours=5, minutes=30)
            p_list["delivery_time"] = d_time.strftime("%Y-%b-%d %I:%M %p")
        else:
            p_list["delivery_time"] = None
        p_list["taxes"] = order_record[0].taxes
        p_list["sub_total"] = order_record[0].sub_total
        p_list["total_bill_value"] = order_record[0].total_bill_value
        p_list["special_instructions"] = order_record[0].special_instructions
        p_list["is_rider_assign"] = order_record[0].is_rider_assign
        p_list["other_order_id"] = order_record[0].outlet_order_id
        p_list["urban_order_id"] = order_record[0].urban_order_id
        p_list["channel_order_id"] = order_record[0].channel_order_id
        p_list["cancel_reason"] = order_record[0].order_cancel_reason
        p_list["delivery_instructions"] = order_record[0].delivery_instructions
        p_list["cancel_responsibility"] = order_record[0].cancel_responsibility
        p_list["delivery_charge"] = order_record[0].delivery_charge
        p_list["packing_charge"] = order_record[0].packing_charge
        p_list["rider_id"] = order_record[0].delivery_boy_id
        p_list["discount_name"]  = order_record[0].discount_name
        p_list["discount_value"] = order_record[0].discount_value
        p_list["coupon_code"] = order_record[0].coupon_code
        if p_list['coupon_code']:
            if 'discount' in order_record[0].order_description[0]:
                p_list["discount_value"] =order_record[0].order_description[0]['discount']
            p_list["discount_name"] = order_record[0].coupon_code
        p_list["rider_detail"] = []
        if order_record[0].is_rider_assign == True:
            if order_record[0].is_aggregator == False:
                a = {}
                ad = ManagerProfile.objects.filter(id=order_record[0].delivery_boy_id)
                a["name"] = ad[0].manager_name
                a["email"] = ad[0].email
                a["mobile"] = ad[0].mobile
                p_list["rider_detail"].append(a)
            else:
                rider_detail = order_record[0].delivery_boy_details
                p_list["rider_detail"].append(rider_detail)
        else:
            a = {}
            a["name"] = ""
            a["email"] = ""
            a["mobile"] = ""
            p_list["rider_detail"].append(a)
        p_list["address"] = []
        if len(order_record[0].address) > 0:
            for index in order_record[0].address:
                dic = {}
                if 'city' in index:
                    try:
                        city = int(index["city"])
                        city_data = CityMaster.objects.filter(id=index['city'])
                        if city_data.count() > 0:
                            dic['city'] = city_data[0].city
                        else:
                            dic['city'] = index['city']
                    except Exception as e:
                        dic['city'] = index['city']
                if 'locality' in index:
                    try:
                        locality = int(index["locality"])
                        city_data = CityMaster.objects.filter(id=index['city'])
                        locality_data = AreaMaster.objects.filter(id=index['locality'])
                        if locality_data.count() > 0:
                            dic['locality'] = locality_data[0].area
                        else:
                            dic['locality'] = index['locality']
                    except Exception as e:
                        dic['locality'] = index['locality']
                if 'address' in index:
                    dic['address'] = index['address']
                else:
                    dic['address'] = ''
                if 'address_type' in index:
                    dic['address_type'] = index['address_type']
                else:
                    dic['address_type'] = ''
                p_list['address'].append(dic)
        final_result.append(p_list)
        err = {
            "success": True,
            "message": "Order data retrieval api worked well!!",
            "data": final_result,
        }
    return err