from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

import stripe
from checkout.webhook_handler import StripeWH_Handler


@require_POST
@csrf_exempt
def webhook(request):
    """Listen for webhooks from Stripe"""
    # Setup
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Get the webhook data and verify its signature
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    event = None

    try:
        # Verify the event signature and parse the event
        event = stripe.Webhook.construct_event(payload, sig_header, wh_secret)
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)
    except Exception as e:
        # Handle other exceptions
        return HttpResponse(content=str(e), status=400)

    # Initialize the webhook handler
    handler = StripeWH_Handler(request)

    # Map webhook events to relevant handler functions
    event_map = {
        "payment_intent.succeeded": handler.handle_payment_intent_succeeded,
        "payment_intent.failed": handler.handle_payment_intent_failed,
    }

    # Get the webhook type from Stripe
    event_type = event.get("type")

    # Retrieve the event handler based on the event type or use a generic handler
    event_handler = event_map.get(event_type, handler.handle_event)

    # Call the event handler with the event data
    response = event_handler(event)
    return response
