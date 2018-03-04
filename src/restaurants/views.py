# Create your views here.
from django.db.models import Q
from django.shortcuts import render
from .models import RestaurantLocation
from django.views.generic.list import ListView


def restaurant_listview(request):
    template_name = 'restaurants/restaurantlocation_list.html'
    queryset = RestaurantLocation.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, template_name, context)


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
