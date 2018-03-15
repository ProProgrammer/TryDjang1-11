# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, UpdateView
from django.views.generic.list import ListView

from .forms import RestaurantLocationCreateForm
from .models import RestaurantLocation


class RestaurantListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return RestaurantLocation.objects.filter(owner=self.request.user)


class RestaurantDetailView(LoginRequiredMixin, DetailView):
    def get_queryset(self):
        return RestaurantLocation.objects.filter(owner=self.request.user)


class RestaurantCreateView(LoginRequiredMixin, CreateView):
    form_class = RestaurantLocationCreateForm
    # The login_url variable here will override the one that we have set in default settings (base.py)
    login_url = '/login/'  # We are keeping it same for now. But in case someone changes there, it will remain Login
    #  for this view always until we change it here too or remove this variable altogether.
    template_name = 'form.html'

    # success_url = '/restaurants'

    # Overriding form_valid method while implementing class based authentication
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        # instance.save()

        return super(RestaurantCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RestaurantCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Add Restaurant'
        return context


class RestaurantUpdateView(LoginRequiredMixin, UpdateView):
    form_class = RestaurantLocationCreateForm
    # The login_url variable here will override the one that we have set in default settings (base.py)
    login_url = '/login/'  # We are keeping it same for now. But in case someone changes there, it will remain Login
    #  for this view always until we change it here too or remove this variable altogether.
    template_name = 'restaurants/detail-update.html'

    # success_url = '/restaurants'

    # Overriding form_valid method while implementing class based authentication

    def get_context_data(self, **kwargs):
        context = super(RestaurantUpdateView, self).get_context_data(**kwargs)
        context['title'] = f'Update Restaurant: {self.get_object().name}'
        return context

    def get_queryset(self):
        return RestaurantLocation.objects.filter(owner=self.request.user)
