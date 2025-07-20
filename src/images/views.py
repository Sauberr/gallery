from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView

from common.mixins import CacheMixin, TitleMixin
from core.utils.paginator import paginator
from images.forms import ImageCreateForm
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
                UserSubscription.objects.select_related("plan").only("plan__name").get(user=self.request.user)
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
                UserSubscription.objects.select_related("plan").only("plan__name").get(user=self.request.user)
            )
            user_subscription_plan = user_subscription.plan.name
            allowed_plans = self.ALLOWED_PLANS
        except UserSubscription.DoesNotExist:
            pass

        context["user_subscription_plan"] = user_subscription_plan
        context["allowed_plans"] = allowed_plans

        return context


class ImageCreateView(LoginRequiredMixin, TitleMixin, CreateView):
    model = Images
    form_class = ImageCreateForm
    template_name: str = "partials/feature.html"
    title: str = "Feature Image"
    success_url = reverse_lazy("images:image-list")

    def form_valid(self, form):
        messages.success(self.request, "Image created successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)
