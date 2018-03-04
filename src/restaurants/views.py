# Create your views here.
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.list import ListView

from .forms import RestaurantCreateForm
from .models import RestaurantLocation


def restaurant_createview(request):
    form = RestaurantCreateForm(request.POST or None)
    errors = None
    if form.is_valid():
        obj = RestaurantLocation.objects.create(
            name=form.cleaned_data.get("name"),
            location=form.cleaned_data.get("location"),
            category=form.cleaned_data.get("category")
        )
        return HttpResponseRedirect("/restaurants")
    if form.errors:
        errors = form.errors

    template_name = 'restaurants/form.html'
    context = {'form': form, 'errors': errors}
    return render(request, template_name, context)


# def restaurant_listview(request):
#     template_name = 'restaurants/restaurantlocation_list.html'
#     queryset = RestaurantLocation.objects.all()
#     context = {
#         'object_list': queryset
#     }
#     return render(request, template_name, context)


class RestaurantListView(ListView):
    def get_queryset(self):
        slug = self.kwargs.get('slug')

        queryset = RestaurantLocation.objects.all()

        if slug:
            return queryset.filter(
                Q(category__iexact=slug) |
                Q(category__icontains=slug)
            )
        return queryset


class RestaurantDetailView(DetailView):
    queryset = RestaurantLocation.objects.all()
