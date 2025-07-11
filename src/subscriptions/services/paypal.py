import json
import logging
import os
from http import HTTPStatus
from typing import Dict

import requests

from subscriptions.models import SubscriptionPlan, UserSubscription


def get_paypal_headers(access_token: str) -> Dict[str, str]:
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }


def get_access_token() -> str | None:
    data: Dict[str, str] = {"grant_type": "client_credentials"}

    headers = {"Accept": "application/json", "Accept-Language": "en_US"}

    client_id: str = str(os.environ.get("PAYPAL_CLIENT_ID"))
    secret_id: str = str(os.environ.get("PAYPAL_SECRET_ID"))
    url: str = f"{os.environ.get('PAYPAL_URL')}/v1/oauth2/token"

    try:
        response = requests.post(
            url, data=data, headers=headers, auth=(client_id, secret_id)
        )
        response.raise_for_status()
        return response.json()["access_token"]
    except (requests.exceptions.RequestException, KeyError) as e:
        logging.error(f"Error obtaining access token: {e}")
        return None


def cancel_subscription_paypal(access_token, subscription_id: str) -> None:

    try:
        url: str = (
            f"{os.environ.get('PAYPAL_URL')}/v1/billing/subscriptions/{subscription_id}/cancel"
        )
        requests.post(url, headers=get_paypal_headers(access_token))

    except requests.exceptions.RequestException as e:
        logging.error(f"Error cancelling subscription: {e}")
        return None


def update_subscription_paypal(
    access_token, subscription_id: str, new_plan: str
) -> str | None:

    try:
        user_subscription = UserSubscription.objects.select_related("plan").get(
            paypal_subscription_id=subscription_id
        )
        current_plan = user_subscription.plan.name

        new_subscription_plan = SubscriptionPlan.objects.get(name=new_plan)
        new_subscription_plan_id = new_subscription_plan.paypal_plan_id

        url: str = (
            f'{os.environ.get("PAYPAL_URL")}/v1/billing/subscriptions/{subscription_id}/revise'
        )

        revision_data: Dict[str, any] = {
            "plan_id": new_subscription_plan_id,
        }

        response = requests.post(
            url,
            headers=get_paypal_headers(access_token),
            data=json.dumps(revision_data),
        )
        response_data = response.json()

        if response.status_code == HTTPStatus.OK:
            for link in response_data.get("links", []):
                if link.get("rel") == "approve":
                    return link["href"]
        return None

    except (UserSubscription.DoesNotExist, SubscriptionPlan.DoesNotExist) as e:
        logging.error(f"Error updating subscription: {e}")
        return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error making PayPal request: {e}")
        return None


def get_current_subscription(access_token, subscription_id: str) -> str | None:

    url: str = (
        f"{os.environ.get('PAYPAL_URL')}/v1/billing/subscriptions/{subscription_id}"
    )

    try:
        response = requests.get(url, headers=get_paypal_headers(access_token))

        if response.status_code == HTTPStatus.OK:
            subscription_data = response.json()
            return subscription_data["plan_id"]
        return None

    except requests.exceptions.RequestException as e:
        logging.error(f"Error getting subscription details: {e}")
        return None
