import os

import requests
from http import HTTPStatus
import json
from typing import Dict, Literal
import logging

from subscriptions.models import Subscription


def get_access_token() -> str | None:
    data: Dict[str, str] = {'grant_type': 'client_credentials'}

    headers = {'Accept': 'application/json', 'Accept-Language': 'en_US'}

    client_id: str = str(os.environ.get('PAYPAL_CLIENT_ID'))
    secret_id: str = str(os.environ.get('PAYPAL_SECRET_ID'))
    url: str = f'{os.environ.get('PAYPAL_URL')}/v1/oauth2/token'

    try:
        response = requests.post(url, data=data, headers=headers, auth=(client_id, secret_id))
        response.raise_for_status()
        access_token = response.json()['access_token']
        return access_token
    except requests.exceptions.RequestException as e:
        logging.error(f'Error obtaining access token: {e}')
        return None
    except KeyError as e:
        logging.error(f'Error obtaining access token: {e}')
        return None


def cancel_subscription_paypal(access_token, subscription_id: str) -> None:
    bearer_token: str = f'Bearer {access_token}'

    headers: Dict[str, str] = {
        'Content-Type': 'application/json',
        'Authorization': bearer_token,
    }

    try:
        url: str = f'{os.environ.get('PAYPAL_URL')}/v1/billing/subscriptions/{subscription_id}/cancel'
        response = requests.post(url, headers=headers)

    except requests.exceptions.RequestException as e:
        logging.error(f'Error cancelling subscription: {e}')
        return None


def update_subscription_paypal(access_token, subscription_id: str, new_plan: str) ->  str | None:
    bearer_token: str = f'Bearer {access_token}'

    headers: Dict[str, str] = {
        'Content-Type': 'application/json',
        'Authorization': bearer_token,
    }

    subscriptions_details = Subscription.objects.get(paypal_subscription_id=subscription_id)
    current_subscription_plan = subscriptions_details.subscription_plan

    PlanType = Literal['Basic', 'Premium', 'Enterprise']
    PlanMapping = Dict[PlanType, Dict[PlanType, str]]

    plan_mapping: PlanMapping = {
        'Basic': {
            'Premium': os.environ.get('PREMIUM'),
            'Enterprise': os.environ.get('ENTERPRISE'),
        },
        'Premium': {
            'Basic': os.environ.get('BASIC'),
            'Enterprise': os.environ.get('ENTERPRISE'),
        },
        'Enterprise': {
            'Basic': os.environ.get('BASIC'),
            'Premium': os.environ.get('PREMIUM'),
        }
    }

    new_subscription_plan_id = plan_mapping.get(current_subscription_plan, {}).get(new_plan)

    url: str = f'{os.environ.get("PAYPAL_URL")}/v1/billing/subscriptions/{subscription_id}/revise'

    revision_data: Dict[str, str] = {
        'plan_id': new_subscription_plan_id,
    }

    response = requests.post(url, headers=headers, data=json.dumps(revision_data))

    response_data = response.json()

    approval_url = None

    for link in response_data.get('links', []):
        if link.get('rel') == 'approve':
            approval_url = link['href']

    if response.status_code == HTTPStatus.OK:
        return approval_url

    else:
        return None


def get_current_subscription(access_token, subscription_id: str) -> str | None:
    bearer_token: str = f'Bearer {access_token}'

    headers: Dict[str, str] = {
        'Content-Type': 'application/json',
        'Authorization': bearer_token,
    }

    url: str = f'{os.environ.get('PAYPAL_URL')}/v1/billing/subscriptions/{subscription_id}'

    response = requests.get(url, headers=headers)

    if response.status_code == HTTPStatus.OK:
        subscription_data = response.json()

        current_plan_id = subscription_data['plan_id']

        return current_plan_id

    else:
        return None
