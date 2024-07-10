from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),

]

urlpatterns += [
    path('products/', views.ProductListView.as_view(), name='product'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
]


urlpatterns += [
	path('orders/', views.OrderListView.as_view(), name='order'),
	path('order/<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
]

urlpatterns += [
    path('customers/', views.CustomerListView.as_view(), name='customer'),
	path('customer/<int:pk>', views.CustomerDetailView.as_view(), name='customer-detail'),

]

urlpatterns += [
	path('add_product/', views.add_product, name='add_product'),
    path('add_customer/', views.add_customer, name='add_customer'),
	path('add_order/', views.add_order, name='add_order'),
]


urlpatterns += [
	path('orderitems/', views.OrderItemListView.as_view(), name='orderitem'),

]



