from http import HTTPStatus

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView

from common.mixins import TitleMixin
from .models import SubscriptionPlan, UserSubscription
from .services.paypal import (
    cancel_subscription_paypal,
    get_access_token,
    get_current_subscription,
    update_subscription_paypal
)


class CreateSubscription(LoginRequiredMixin, TitleMixin, View):
    title: str = "Create Subscription"

    def get(self, request, subscription_id: str, plan: str) -> HttpResponse:
        if UserSubscription.objects.filter(user=request.user, is_active=True).exists():
            return HttpResponse("You already have an active subscription", status=HTTPStatus.BAD_REQUEST)

        subscription_plan = get_object_or_404(SubscriptionPlan, name=plan)

        UserSubscription.objects.create(
            user=request.user, plan=subscription_plan, paypal_subscription_id=subscription_id, is_active=True
        )

        context = {"subscription_plan": subscription_plan}
        return render(request, "subscriptions/create_subscription.html", context)


class ConfirmDeleteSubscription(LoginRequiredMixin, TitleMixin, DeleteView):
    model = UserSubscription
    template_name: str = "subscriptions/confirm_delete_subscription.html"
    success_url = reverse_lazy("subscriptions:delete_subscription")
    slug_field: str = "paypal_subscription_id"
    slug_url_kwarg: str = "subscription_id"
    title: str = "Confirm Subscription Deletion"

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subscription_id"] = self.kwargs["subscription_id"]
        return context


class DeleteSubscription(LoginRequiredMixin, TitleMixin, View):

    def get(self, request, subscription_id: str) -> HttpResponse:
        access_token = get_access_token()
        cancel_subscription_paypal(access_token, subscription_id)

        subscription = get_object_or_404(
            UserSubscription,
            user=request.user,
            paypal_subscription_id=subscription_id
        )
        subscription.delete()

        context = {"title": "Subscription Deleted"}
        return render(request, "subscriptions/delete_subscription.html", context)


class UpdateSubscription(LoginRequiredMixin, View):

    def get(self, request, subscription_id: str, new_plan: str) -> HttpResponse:

        subscription = get_object_or_404(
            UserSubscription,
            user=request.user,
            paypal_subscription_id=subscription_id,
            is_active=True
        )

        access_token = get_access_token()
        approve_link = update_subscription_paypal(access_token, subscription_id, new_plan)

        if approve_link:
            return redirect(approve_link)
        return HttpResponse("Unable to obtain the approval link. Please try again later.")


class PaypalUpdateSubscriptionConfirmed(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs) -> HttpResponse:
        try:
            subscription = get_object_or_404(UserSubscription, user=request.user, is_active=True)
            context = {"subscription_id": subscription.paypal_subscription_id}
            return render(request, "subscriptions/paypal_update_subscription_confirmed.html", context)
        except UserSubscription.DoesNotExist:
            return render(request, "subscriptions/paypal_update_subscription_confirmed.html")


class DjangoUpdateSubscriptionConfirmed(LoginRequiredMixin, View):

    def get(self, request, subscription_id: str) -> HttpResponse:
        try:
            access_token = get_access_token()
            current_plan_id = get_current_subscription(access_token, subscription_id)

            subscription_plan = get_object_or_404(
                SubscriptionPlan,
                paypal_plan_id=current_plan_id
            )

            updated = UserSubscription.objects.filter(
                user=request.user,
                paypal_subscription_id=subscription_id
            ).update(
                plan=subscription_plan,
                is_active=True
            )

            if not updated:
                return HttpResponse("Subscription not found", status=HTTPStatus.NOT_FOUND)

            return render(request, "subscriptions/django_update_subscription_confirmed.html")

        except UserSubscription.DoesNotExist:
            return HttpResponse("Subscription not found", status=HTTPStatus.NOT_FOUND)
