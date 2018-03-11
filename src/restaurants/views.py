# Create your views here.
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView, CreateView
from django.views.generic.list import ListView

from .forms import RestaurantLocationCreateForm
from .models import RestaurantLocation


@login_required(login_url='/login/')
def restaurant_createview(request):
    form = RestaurantLocationCreateForm(request.POST or None)
    errors = None
    if form.is_valid():
        if request.user.is_authenticated():
            # Turn this form into potential instance, or instance that's going to happen and just hasn't saved yet.
            instance = form.save(commit=False)  # So we have an instance but we're not quite saving it yet(commit=False)

            # customize
            # pre_save signals
            # form.save()

            # So now that I have an instance, I could say:
            instance.owner = request.user
            instance.save()

            # post_save signals
            # obj = RestaurantLocation.objects.create(
            #     name=form.cleaned_data.get("name"),
            #     location=form.cleaned_data.get("location"),
            #     category=form.cleaned_data.get("category")
            # )

            return HttpResponseRedirect("/restaurants")
        else:
            return HttpResponseRedirect('/login/')
            # Redirect to login in case user is not authenticated.
            # This is not the best practice, but just an example of how it can be done

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


class RestaurantCreateView(CreateView):
    form_class = RestaurantLocationCreateForm
    template_name = 'restaurants/form.html'
    success_url = '/restaurants'

    # Overriding form_valid method while implementing class based authentication
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        # instance.save()

        return super(RestaurantCreateView, self).form_valid(form)
