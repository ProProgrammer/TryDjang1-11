import random

from django.views.generic import TemplateView


# Create your views here.


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        num = None
        some_list = [
            random.randint(0, 1000000),
            random.randint(0, 1000000),
            random.randint(0, 1000000),
        ]

        condition_bool_item = True

        if condition_bool_item:
            num = random.randint(0, 1000000)
        context['num'] = num
        context['some_list'] = some_list
        return context
