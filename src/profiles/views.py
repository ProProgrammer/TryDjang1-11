from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView
from .models import Profile
from menus.models import Item
from restaurants.models import RestaurantLocation

User = get_user_model()


class ProfileFollowToggle(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        # print(request.data)
        # print(request.POST)
        user_to_toggle = request.POST.get('username')
        print(user_to_toggle)
        profile_ = Profile.objects.get(user__username__iexact=user_to_toggle)
        user = request.user
        print('requested user:', user)
        if user in profile_.followers.all():
            profile_.followers.remove(user)
        else:
            profile_.followers.add(user)
        return redirect("/")


class ProfileDetailView(DetailView):
    template_name = 'profiles/user.html'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        if username is None:
            raise Http404
        return get_object_or_404(User, username__iexact=username, is_active=True)

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        # print(context)
        user = context['user']
        query = self.request.GET.get('q')
        items_exists = Item.objects.filter(user=user).exists()
        qs = RestaurantLocation.objects.filter(owner=user).search(query)

        if items_exists and qs.exists():
            context['locations'] = qs
        return context

# >>> deep_user.is_following.all()
# <QuerySet [<Profile: random-test>, <Profile: deep>, <Profile: admin>, <Profile: user_5>]>
# <QuerySet [<Profile: random-test>, <Profile: deep>, <Profile: user_5>]>
