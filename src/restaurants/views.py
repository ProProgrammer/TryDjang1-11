# Create your views here.
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.list import ListView
from .forms import RestaurantCreateForm
from .models import RestaurantLocation
from django.http import HttpResponseRedirect


def restaurant_createview(request):
    # if request.method == "GET":
    #     print("GET Data")
    if request.method == "POST":  # PUT
        print("POST Data")
        print(request.POST)
        title = request.POST.get("title")
        location = request.POST.get('location')
        category = request.POST.get('category')
        obj = RestaurantLocation.objects.create(
            name=title,
            location=location,
            category=category
        )
        return HttpResponseRedirect("/restaurants")
    template_name = 'restaurants/form.html'
    context = {}
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
