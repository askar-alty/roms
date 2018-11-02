from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from ratelimit.decorators import ratelimit
from rest_framework import (views,
                            generics,
                            permissions as django_permissions,
                            response,
                            status)
from reversion.models import Version

from . import (models, forms, serializers, mixins, permissions, auth)
from ..restaurants.models import Order


def index(request):
    return render(template_name='index.html', request=request)


@login_required(login_url='/accounts/login/')
def content_management(request):
    versions = Version.objects.all().order_by('-revision__date_created')[:30]
    versions = [v for v in versions]
    return render(request=request,
                  context={
                      'versions': versions
                  },
                  template_name='management/content-management.html')


class UserCreateView(mixins.RequiredMixin, generic.CreateView):
    model = User
    fields = '__all__'
    template_name = 'employees/create-user.html'
    success_url = reverse_lazy('create_employee')
    permission_required = ('accounts.add_employee',)


class EmployeeListView(mixins.RequiredMixin, mixins.RevisionMixin, generic.ListView):
    model = models.Employee
    template_name = 'employees/employee-list.html'
    context_object_name = 'employees'


class EmployeeCreateView(mixins.RequiredMixin, mixins.RevisionMixin, generic.CreateView):
    model = models.Employee
    fields = '__all__'
    template_name = 'employees/create-employee.html'
    success_url = reverse_lazy('employees')
    permission_required = ('accounts.add_employee',)


class EmployeeUpdateView(mixins.RequiredMixin, mixins.RevisionMixin, generic.UpdateView):
    model = models.Employee
    fields = '__all__'
    template_name = 'employees/update-employee.html'
    permission_required = ('accounts.change_employee',)

    def get_success_url(self):
        return reverse_lazy('update_employee', kwargs={'pk': self.kwargs['pk']})

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs['pk'])


class LoginAPIView(views.APIView):
    permission_classes = (django_permissions.AllowAny,)

    @ratelimit(key='ip', block=True, rate='10/m', method='POST')
    def post(self, request):
        form = forms.AuthenticationForm(request.data)
        if form.is_valid():
            user = authenticate(request, username=form.get_username(), password=form.get_password())
            if user is not None:
                login(request, user)
                token = models.AuthToken.objects.get_or_create(user=user)
                return response.Response(status=status.HTTP_201_CREATED,
                                         data=serializers.AuthTokenSerializer(token).data)
            else:
                return response.Response(status=status.HTTP_401_UNAUTHORIZED,
                                         data={'detail': 'User with name {} not found'.format(form.get_username())})

        return response.Response(status=status.HTTP_401_UNAUTHORIZED,
                                 data={'detail': 'Incorrect credentials'})


class EmployeeAPIListView(generics.ListAPIView):
    authentication_classes = (auth.TokenAuth,)
    permission_classes = (permissions.OrderPermissions,)
    serializer_class = serializers.EmployeeReadSerializer

    def get_queryset(self):
        return models.Employee.objects.all()
