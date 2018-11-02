from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    url(r'^restaurants/$', views.RestaurantListViews.as_view(), name='restaurants'),
    url(r'^orders/$', views.OrderListView.as_view(), name='orders'),
    url(r'^dish-items/$', views.DishItemListView.as_view(), name='dish_items'),

    url(r'^restaurants/create/$', views.RestaurantCreateView.as_view(), name='create_restaurant'),
    url(r'^orders/create/$', views.OrderCreateView.as_view(), name='create_order'),
    url(r'^dish-items/create/$', views.DishItemCreateView.as_view(), name='create_dish_item'),

    url(r'^restaurants/(?P<pk>\d+)/update/$', views.RestaurantUpdateView.as_view(), name='update_restaurant'),
    url(r'^orders/(?P<pk>\d+)/update/$', views.OrderUpdateView.as_view(), name='update_order'),
    url(r'^dish-items/(?P<pk>\d+)/update/$', views.DishItemUpdateView.as_view(), name='update_dish_item'),

    # API urls
    url(r'^api/restaurants/$', views.RestaurantAPIListView.as_view(), name='api_restaurants'),
    url(r'^api/dish-items/$', views.DishItemAPIListView.as_view(), name='api_dish_items'),
    url(r'^api/dish-items/create/$', views.DishItemCreateAPIView.as_view(), name='api_create_dish_items'),
    url(r'^api/orders/$', views.OrderListAPIView.as_view(), name='api_orders'),
    url(r'^api/orders/create/$', views.OrderCreateAPIView.as_view(), name='api_create_order'),
    url(r'^api/orders/(?P<pk>\d+)/$', views.OrderUpdateAPIView.as_view(), name='api_update_order'),

]
