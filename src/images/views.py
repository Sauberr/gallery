from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from common.mixins import CacheMixin, TitleMixin
from core.utils.paginator import paginator
from images.models import Images
from subscriptions.models import UserSubscription


class ImagesList(LoginRequiredMixin, CacheMixin, TitleMixin, ListView):
    template_name: str = "images/images.html"
    title: str = "Gallery"
    model = Images
    context_object_name: str = "images"
    ordering = ["title"]

    ALLOWED_PLANS = {
        "Basic": ["Basic"],
        "Premium": ["Basic", "Premium"],
        "Enterprise": ["Basic", "Premium", "Enterprise"],
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_subscription_plan = None
        allowed_plans = {}

        try:
            user_subscription = (
                UserSubscription.objects
                .select_related('plan')
                .only('plan__name')
                .get(user=self.request.user)
            )
            user_subscription_plan = user_subscription.plan.name
            allowed_plans = self.ALLOWED_PLANS
        except UserSubscription.DoesNotExist:
            pass

        context["user_subscription_plan"] = user_subscription_plan
        context["allowed_plans"] = allowed_plans

        images = self.get_queryset()
        custom_range, images = paginator(self.request, images, 4)
        context["custom_range"] = custom_range
        context["images"] = self.set_get_cache(images, "images", 15)

        return context

class ImageDetail(LoginRequiredMixin, TitleMixin, DetailView):
    template_name: str = "images/image-detail.html"
    title: str = "Image Detail"
    model = Images
    context_object_name: str = "image"

    ALLOWED_PLANS = {
        "Basic": ["Basic"],
        "Premium": ["Basic", "Premium"],
        "Enterprise": ["Basic", "Premium", "Enterprise"],
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_subscription_plan = None
        allowed_plans = {}

        try:
            user_subscription = (
                UserSubscription.objects
                .select_related('plan')
                .only('plan__name')
                .get(user=self.request.user)
            )
            user_subscription_plan = user_subscription.plan.name
            allowed_plans = self.ALLOWED_PLANS
        except UserSubscription.DoesNotExist:
            pass

        context["user_subscription_plan"] = user_subscription_plan
        context["allowed_plans"] = allowed_plans

        return context
