import os
from typing import Dict, Final, Literal, Tuple

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView

from common.mixins import TitleMixin
from subscriptions.models import Enterprise, Subscription
from subscriptions.services.paypal import (cancel_subscription_paypal,
                                           get_access_token,
                                           get_current_subscription,
                                           update_subscription_paypal)

BASIC: Final = "Basic"
PREMIUM: Final = "Premium"
ENTERPRISE: Final = "Enterprise"

BASIC_COST: Final = "4.99"
PREMIUM_COST: Final = "9.99"
ENTERPRISE_COST: Final = "14.99"


class CreateSubscription(TitleMixin, View):
    title: str = "Create Subscription"

    def get(self, request, subscription_id: str, plan: str) -> HttpResponse:
        user = get_user_model().objects.get(email=request.user.email)
        first_name, last_name = user.first_name, user.last_name
        full_name = f"{first_name} {last_name}"

        selected_subscription_plan = plan

        plan_mapping: Dict[str, str] = {
            BASIC: BASIC_COST,
            PREMIUM: PREMIUM_COST,
            Enterprise: ENTERPRISE_COST,
        }

        subscription_cost = plan_mapping.get(selected_subscription_plan)

        subscriptions = Subscription.objects.create(
            subscriber_name=full_name,
            subscription_plan=selected_subscription_plan,
            subscription_cost=subscription_cost,
            paypal_subscription_id=subscription_id,
            is_active=True,
            user=request.user,
        )

        context = {"subscription_plan": selected_subscription_plan}

        return render(request, "subscriptions/create_subscription.html", context)


class ConfirmDeleteSubscription(LoginRequiredMixin, TitleMixin, DeleteView):
    model = Subscription
    template_name: str = "subscriptions/confirm_delete_subscription.html"
    success_url = reverse_lazy("subscriptions:delete_subscription")
    slug_field: str = "paypal_subscription_id"
    slug_url_kwarg: str = "subscription_id"
    title = "Confirm Subscription Deletion"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subscription_id"] = self.kwargs["subscription_id"]
        return context


class DeleteSubscription(LoginRequiredMixin, TitleMixin, View):

    def get(self, request, subscription_id: str) -> HttpResponse:
        access_token = get_access_token()
        cancel_subscription_paypal(access_token, subscription_id)

        subscription = Subscription.objects.get(user=request.user, paypal_subscription_id=subscription_id)
        subscription.delete()
        context = {"title": "Subscription Deleted"}

        return render(request, "subscriptions/delete_subscription.html", context)


class UpdateSubscription(View):

    def get(self, request, subscription_id: str, new_plan: str) -> HttpResponse:
        access_token = get_access_token()
        approve_link = update_subscription_paypal(access_token, subscription_id, new_plan)
        if approve_link:
            return redirect(approve_link)
        else:
            return HttpResponse("Unable to obtain the approval link. Please try again later.")


class PaypalUpdateSubscriptionConfirmed(View):

    def get(self, request, *args, **kwargs) -> HttpResponse:
        try:
            subscription_details = Subscription.objects.get(user=request.user)
            subscription_id = subscription_details.paypal_subscription_id

            context = {"subscription_id": subscription_id}
            return render(request, "subscriptions/paypal_update_subscription_confirmed.html", context)
        except Subscription.DoesNotExist:
            return render(request, "subscriptions/paypal_update_subscription_confirmed.html")


class DjangoUpdateSubscriptionConfirmed(View):

    def get(self, request, subscription_id: str) -> HttpResponse:

        try:
            access_token = get_access_token()
            current_plan_id = get_current_subscription(access_token, subscription_id)

            plan_mapping = {
                os.environ.get("BASIC"): (BASIC, BASIC_COST),
                os.environ.get("PREMIUM"): (PREMIUM, PREMIUM_COST),
                os.environ.get("ENTERPRISE"): (ENTERPRISE, ENTERPRISE_COST),
            }

            new_plan = plan_mapping.get(current_plan_id)
            if new_plan:
                new_plan_name, new_plan_cost = new_plan
                subscription = Subscription.objects.filter(paypal_subscription_id=subscription_id).update(
                    subscription_plan=new_plan_name, subscription_cost=new_plan_cost
                )
            return render(request, "subscriptions/django_update_subscription_confirmed.html")

        except Subscription.DoesNotExist:
            pass
