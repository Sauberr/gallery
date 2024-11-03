from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from common.mixins import CacheMixin, TitleMixin
from core.utils.paginator import paginator
from images.models import Images


class ImagesList(LoginRequiredMixin, CacheMixin, TitleMixin, ListView):
    template_name: str = "images/images.html"
    title: str = "Gallery"
    model = Images
    context_object_name: str = "images"
    ordering = ["title"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_subscription_plan = None
        allowed_plans = {}

        if hasattr(self.request.user, "subscription"):
            user_subscription_plan = self.request.user.subscription.subscription_plan
            allowed_plans = {
                "Basic": ["Basic"],
                "Premium": ["Basic", "Premium"],
                "Enterprise": ["Basic", "Premium", "Enterprise"],
            }

        context["user_subscription_plan"] = user_subscription_plan
        context["allowed_plans"] = allowed_plans

        images = self.get_queryset()
        custom_range, images = paginator(self.request, images, 4)
        context["custom_range"] = custom_range
        context["images"] = self.set_get_cache(images, "images", 15)

        return context
