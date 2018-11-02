from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^categories/$', views.CategoryListView.as_view(), name='categories'),
    url(r'^dishes/$', views.DishListView.as_view(), name='dishes'),

    url(r'^categories/create/$', views.CategoryCreateView.as_view(), name='create_category'),
    url(r'^dishes/create/$', views.DishCreateView.as_view(), name='create_dish'),

    url(r'^categories/(?P<pk>\d+)/update/$', views.CategoryUpdateView.as_view(), name='update_category'),
    url(r'^dishes/(?P<pk>\d+)/update/$', views.DishUpdateView.as_view(), name='update_dish'),

    # API urls
    url(r'^api/dishes/$', views.DishAPIListView.as_view(), name='api_dishes')
]
