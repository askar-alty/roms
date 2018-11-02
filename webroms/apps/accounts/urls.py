from django.conf.urls import url
from django.contrib.auth.views import LogoutView, LoginView

from . import views

urlpatterns = [

    # API urls
    url(r'api/login', views.LoginAPIView.as_view(), name='api_login'),

    # UI urls

    url(r'^$', views.index, name='home'),

    url(r'^accounts/login/$', LoginView.as_view(template_name='auth/login.html'), name='login'),
    url(r'^accounts/logout/$', LogoutView.as_view(), name='logout'),

    url(r'^content/management/$', views.content_management, name='content_management'),
    url(r'^employees/$', views.EmployeeListView.as_view(), name='employees'),
    url(r'^employees/create/user/$', views.UserCreateView.as_view(), name='create_user'),
    url(r'^employees/create/$', views.EmployeeCreateView.as_view(), name='create_employee'),
    url(r'^employees/(?P<pk>\d+)/update/$', views.EmployeeUpdateView.as_view(), name='update_employee'),

    # API views

    url(r'^api/employees/$', views.EmployeeAPIListView.as_view(), name='api_employees')
]
