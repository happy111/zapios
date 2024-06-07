# from django.urls import path
# from ZapioApi.Api.webhooks.store import StoreSync
# from ZapioApi.Api.webhooks.store_action import StoreAction
# from ZapioApi.Api.webhooks.inventory import InventorySync
# from ZapioApi.Api.webhooks.order_live import LiveOrders
# from ZapioApi.Api.webhooks.order_status_update import OrderStatusUpdate
# from ZapioApi.Api.webhooks.rider_status_update import RiderStatusUpdate
# from ZapioApi.Api.webhooks.item_toggle import ItemToggle

# urlpatterns = [

# 	path('store/create_update/',StoreSync.as_view()),
# 	path('store/action/',StoreAction.as_view()),
# 	path('inventory/create_update/',InventorySync.as_view()),
# 	path('OrderRelay/live/',LiveOrders.as_view()),
# 	path('Order/status_update/',OrderStatusUpdate.as_view()),
# 	path('rider/status_update/',RiderStatusUpdate.as_view()),
# 	path('item_state/change/',ItemToggle.as_view()),


# ]