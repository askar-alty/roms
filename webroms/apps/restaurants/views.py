from reversion import revisions
from django.views import generic
from django.conf import settings
from django.core import paginator
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from rest_framework import (generics, response, status)

from . import (models, mixins, permissions, serializers)
from ..accounts import auth


# Here are List views


class RestaurantListViews(mixins.RequiredMixin, generic.ListView):
    model = models.Restaurant
    paginator_class = paginator.Paginator
    paginate_by = settings.PAGE_BY
    template_name = 'restaurants/restaurant-list.html'
    context_object_name = 'restaurants'


class OrderListView(mixins.RequiredMixin, generic.ListView):
    model = models.Order
    paginator_class = paginator.Paginator
    paginate_by = settings.PAGE_BY
    template_name = 'restaurants/order-list.html'
    context_object_name = 'orders'


class DishItemListView(mixins.RequiredMixin, generic.ListView):
    model = models.DishItem
    paginator_class = paginator.Paginator
    paginate_by = settings.PAGE_BY
    template_name = 'restaurants/dish-item-list.html'
    context_object_name = 'dish_items'


# Here are Create views

class RestaurantCreateView(mixins.RequiredMixin, generic.CreateView):
    model = models.Restaurant
    fields = '__all__'
    template_name = 'restaurants/create-restaurant.html'
    permission_required = ('restaurants.add_restaurant',)

    def get_success_url(self):
        return reverse_lazy('update_restaurant', kwargs={'pk': self.object.pk})


class OrderCreateView(mixins.RequiredMixin, mixins.RevisionMixin, generic.CreateView):
    model = models.Order
    fields = ('restaurant', 'employee', 'dishes', 'status',)
    template_name = 'restaurants/create-order.html'
    permission_required = ('restaurants.add_order',)

    def get_success_url(self):
        return reverse_lazy('update_order', kwargs={'pk': self.object.pk})


class DishItemCreateView(mixins.RequiredMixin, mixins.RevisionMixin, generic.CreateView):
    model = models.DishItem
    fields = ('dish', 'total',)
    template_name = 'restaurants/create-dish-item.html'
    success_url = reverse_lazy('dish_items')
    permission_required = ('restaurants.add_dishitem',)

    def form_valid(self, form):
        self.object, _ = self.model.objects.get_or_create(**form.cleaned_data)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('update_dish_item', kwargs={'pk': self.object.pk})


# Here are Update views

class RestaurantUpdateView(generic.UpdateView):
    model = models.Restaurant
    fields = '__all__'
    template_name = 'restaurants/update-restaurant.html'
    success_url = reverse_lazy('restaurants')
    permission_required = ('restaurants.change_restaurant',)

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs['pk'])


class OrderUpdateView(mixins.RequiredMixin, mixins.RevisionMixin, generic.UpdateView):
    model = models.Order
    fields = ('restaurant', 'employee', 'dishes', 'status',)
    template_name = 'restaurants/update-order.html'
    success_url = reverse_lazy('orders')
    permission_required = ('restaurants.change_order',)

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs['pk'])


class DishItemUpdateView(mixins.RequiredMixin, mixins.RevisionMixin, generic.UpdateView):
    model = models.DishItem
    fields = ('dish', 'total',)
    template_name = 'restaurants/update-dish-item.html'
    success_url = reverse_lazy('dish_items')
    permission_required = ('restaurants.change_dishitem',)

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs['pk'])


# Here are API views
def get_subset(page, page_by):
    start = (int(page) - 1) * page_by
    return start, start + page_by


class RestaurantAPIListView(generics.ListAPIView):
    authentication_classes = (auth.TokenAuth,)
    permission_classes = (permissions.OrderPermissions,)

    serializer_class = serializers.RestaurantReadSerializer

    def get_queryset(self):
        start, end = get_subset(self.request.data.get('page', 1), settings.PAGE_BY)
        return models.Restaurant.objects.all()[start: end]


class DishItemAPIListView(generics.ListAPIView):
    authentication_classes = (auth.TokenAuth,)
    permission_classes = (permissions.OrderPermissions,)

    serializer_class = serializers.DishItemReadSerializer

    def get_queryset(self):
        start, end = get_subset(self.request.data.get('page', 1), settings.PAGE_BY)
        return models.DishItem.objects.all()[start: end]


class DishItemCreateAPIView(generics.CreateAPIView):
    authentication_classes = (auth.TokenAuth,)
    permission_classes = (permissions.OrderPermissions,)

    serializer_class = serializers.DishItemWriteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(data=serializers.DishItemReadSerializer(serializer.instance).data,
                                 status=status.HTTP_201_CREATED,
                                 headers=headers)


class OrderListAPIView(generics.ListAPIView):
    authentication_classes = (auth.TokenAuth,)
    permission_classes = (permissions.OrderPermissions,)

    serializer_class = serializers.OrderReadSerializer

    def get_queryset(self):
        start, end = get_subset(self.request.data.get('page', 1), settings.PAGE_BY)
        return models.Order.objects.all()[start: end]


class OrderCreateAPIView(generics.CreateAPIView):
    authentication_classes = (auth.TokenAuth,)
    permission_classes = (permissions.IsAuthenticated, permissions.OrderPermissions,)

    serializer_class = serializers.OrderWriteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with revisions.create_revision(manage_manually=True):
            self.perform_create(serializer)
            revisions.set_user(request.user)
            revisions.set_comment('Created by API')
            revisions.set_date_created(serializer.instance)

        headers = self.get_success_headers(serializer.data)
        return response.Response(data=serializers.OrderReadSerializer(serializer.instance).data,
                                 status=status.HTTP_201_CREATED,
                                 headers=headers)


class OrderUpdateAPIView(generics.UpdateAPIView):
    authentication_classes = (auth.TokenAuth,)
    permission_classes = (permissions.IsAuthenticated, permissions.OrderPermissions,)

    serializer_class = serializers.OrderWriteSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with revisions.create_revision(manage_manually=True):
            self.perform_update(serializer)
            revisions.set_user(request.user)
            revisions.set_comment('Created by API')
            revisions.set_date_created(serializer.instance)

        return response.Response(data=serializers.OrderReadSerializer(serializer.instance).data,
                                 status=status.HTTP_200_OK)