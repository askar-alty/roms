from django.conf import settings
from django.views import generic
from django.core import paginator
from django.urls import reverse_lazy
from rest_framework import generics

from . import (models, permissions, serializers, mixins)
from ..accounts import auth


class CategoryListView(mixins.RequiredMixin, generic.ListView):
    model = models.Category
    template_name = 'dishes/category-list.html'
    context_object_name = 'categories'
    permission_required = ('dishes.view_category',)


class DishListView(mixins.RequiredMixin, generic.ListView):
    model = models.Dish
    paginator_class = paginator.Paginator
    paginate_by = settings.PAGE_BY
    template_name = 'dishes/dish-list.html'
    context_object_name = 'dishes'
    permission_required = ('dishes.view_dish',)


class CategoryCreateView(mixins.RequiredMixin, generic.CreateView):
    model = models.Category
    fields = '__all__'
    template_name = 'dishes/create-category.html'
    permission_required = ('dishes.add_category',)

    def get_success_url(self):
        return reverse_lazy('update_category', kwargs={'pk': self.object.pk})

    def get_form(self, form_class=None):
        form = super(CategoryCreateView, self).get_form(form_class)
        form.fields['sub_category'].required = False
        form.fields['description'].required = False
        return form


class DishCreateView(mixins.RequiredMixin, generic.CreateView):
    model = models.Dish
    fields = '__all__'
    template_name = 'dishes/create-dish.html'
    permission_required = ('dishes.add_dish',)

    def get_success_url(self):
        return reverse_lazy('update_dish', kwargs={'pk': self.object.pk})


class CategoryUpdateView(mixins.RequiredMixin, generic.UpdateView):
    model = models.Category
    fields = '__all__'
    template_name = 'dishes/update-category.html'
    permission_required = ('dishes.change_category',)
    success_url = reverse_lazy('categories')

    def get_form(self, form_class=None):
        form = super(CategoryUpdateView, self).get_form(form_class)
        form.fields['sub_category'].required = False
        form.fields['description'].required = False
        return form

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs['pk'])


class DishUpdateView(mixins.RequiredMixin, generic.UpdateView):
    model = models.Dish
    fields = '__all__'
    template_name = 'dishes/update-dish.html'
    permission_required = ('dishes.change_dish',)
    success_url = reverse_lazy('dishes')

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs['pk'])


def get_subset(page, page_by):
    start = (int(page) - 1) * page_by
    return start, start + page_by


class DishAPIListView(generics.ListAPIView):
    authentication_classes = (auth.TokenAuth,)
    permission_classes = (permissions.OrderPermissions,)

    serializer_class = serializers.DishSerializer

    def get_queryset(self):
        start, end = get_subset(self.request.data.get('page', 1), settings.PAGE_BY)
        return models.Dish.objects.all()[start:end]
