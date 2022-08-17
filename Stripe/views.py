from django.shortcuts import HttpResponse
import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.

stripe_sec_key='sk_test_51LVVx1BYA0A64PWfpfrddWzS25OkD6DSfv0utl6lDKBEFuk9jbwgcADLxgnXJcHMc2yQ2VskbbextiqnLOeEAP4C00exjKRLTH'
stripe_pub_key='pk_test_51LVVx1BYA0A64PWf9xSSBckYX9EZAzfMuBFqWJjLEUaoJcpoWsRRrTyEUQ0PWkWbt0a5ekTSeaesFkzZHwMMHL1t00cgZLsBXa'

stripe.api_key=stripe_sec_key

def pay_ammount(request):
    try:
        stripe.PaymentIntent.create(
            amount=1,
            currency='usd',
            payment_method_types=["card"],
        )
    except:
        TypeError("Your payment is failed")


class StripeConfigView(APIView):
    """
    StripeConfigView is the API of configs resource, and
    responsible to handle the requests of /config/ endpoint.
    """
    def get(self, request, format=None):
        config = {
            "publishable_key": str(stripe_pub_key)
        }
        return Response(config)

@api_view(["GET"])
def checkout_stripe(request):
    domain_url = 'http://localhost:8000/'
    sessions = stripe.checkout.Session.create(
        success_url=domain_url+"success",
        cancel_url=domain_url+"failure",
        payment_method_types=['card'],
        mode='payment',
        line_items=[
            {

                'price_data': {
                    'currency': 'usd',
                    'unit_amount': 2000,
                    'product_data': {
                        'name': 'TestProduct',
                        'description': 'Comfortable cotton t-shirt',

                    },
                },
                'quantity': 1,
            }
        ]

    )
    return Response({'sessionId': sessions['url']})



@api_view(["GET"])
def stripe_web_hook(request):
    endpoint_secret = 'whsec_7b5f9af3a604e5566094b1c731217e36877a4855daf607515d5f507ae439009a'
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header
        )
    except ValueError as e:
        # Invalid payload
        return Response(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return Response(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        # TODO: run some custom code here

    return Response(status=200)


def success(request):
    return HttpResponse("Payment is successful")

def failure(request):
    return HttpResponse("Payment is unsuccessful")