from django.http import HttpResponse


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded event
        """
        payment_intent = event.get('data', {}).get('object', {})
        # Process the payment_intent
        return HttpResponse(
            content=f'PaymentIntent succeeded: {payment_intent["id"]}',
            status=200
        )

    def handle_payment_intent_failed(self, event):
        """
        Handle the payment_intent.failed event
        """
        payment_intent = event.get('data', {}).get('object', {})
        # Handle the failed payment intent
        return HttpResponse(
            content=f'PaymentIntent failed: {payment_intent["id"]}',
            status=200
        )