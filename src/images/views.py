from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from common.mixins import TitleMixin
from images.models import Images


class ImagesList(LoginRequiredMixin, TitleMixin, ListView):
    template_name: str = "images/images_list.html"
    title: str = "Gallery"
    model = Images
    context_object_name: str = 'images'
    ordering = ['title']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_subscription_plan = None
        allowed_plans = {}

        if hasattr(self.request.user, 'subscription'):
            user_subscription_plan = self.request.user.subscription.subscription_plan
            allowed_plans = {
                'Basic': ['Basic'],
                'Premium': ['Basic', 'Premium'],
                'Enterprise': ['Basic', 'Premium', 'Enterprise'],
            }

        context['user_subscription_plan'] = user_subscription_plan
        context['allowed_plans'] = allowed_plans
        return context
