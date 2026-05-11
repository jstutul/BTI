import requests
from django.conf import settings
from django.urls import reverse


def get_base_url():
    if settings.BKASH_MODE == "sandbox":
        return "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/"
    return "https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/"


def get_token():
    url = get_base_url() + "checkout/token/grant"
    headers = {
        "Content-Type": "application/json",
        "username": settings.BKASH_USERNAME,
        "password": settings.BKASH_PASSWORD,
    }

    payload = {
        "app_key": settings.BKASH_APP_KEY,
        "app_secret": settings.BKASH_APP_SECRET,
    }
    print(headers,payload)

    res = requests.post(url, json=payload, headers=headers)
    data = res.json()
    print(data)
    return data.get("id_token")


def create_payment(request, amount):
    token = get_token()
    print("Token",token)
    request.session["bkash_token"] = token

    callback_url = request.build_absolute_uri(reverse("dashboard:bkash_callback"))

    url = get_base_url() + "checkout/create"

    headers = {
        "Content-Type": "application/json",
        "Authorization": token,
        "X-APP-Key": settings.BKASH_APP_KEY,
    }

    payload = {
        "mode": "0011",
        "payerReference": str(request.user.id),
        "callbackURL": callback_url,
        "amount": str(amount),
        "currency": "BDT",
        "intent": "sale",
        "merchantInvoiceNumber": f"DEP{request.user.id}",
    }

    res = requests.post(url, json=payload, headers=headers)
    return res.json()


def execute_payment(payment_id, token):
    url = get_base_url() + "checkout/execute"

    headers = {
        "Content-Type": "application/json",
        "Authorization": token,
        "X-APP-Key": settings.BKASH_APP_KEY,
    }

    res = requests.post(url, json={"paymentID": payment_id}, headers=headers)
    return res.json()