from google_speech import Speech
from django.db.models import Q
from Orders.models import Order, OrderStatusType
from Outlet.models import DeliveryBoy,OutletProfile


def soundeffect():
	data = \
		Order.objects.filter(Q(Company=1),Q(is_seen=0)).order_by('-order_time')
	a = " "
	a_dict = {}
	for i in data:
		a_dict = {}
		orderid = i.order_id
		outlet_name = OutletProfile.objects.filter(id=i.outlet_id).first().Outletname
		b = "You have recieved one new order " +orderid+" from "+outlet_name+"."
		a = a + " "+b
	for i in range(2):
		a = a+a
	a_dict['text'] = a
	lang = "en"
	speech = Speech(a_dict['text'], lang)
	sox_effects = ("speed", "1")
	speech.save('media/order.mp3')