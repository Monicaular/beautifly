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
        intent = event.data.object
        pid = intent.id
        basket = intent.metadata.basket
        save_info = intent.metadata.save_info

        # Get the Charge object
        stripe_charge = stripe.Charge.retrieve(intent.latest_charge)

        billing_details = stripe_charge.billing_details
        shipping_details = intent.shipping
        grand_total = round(stripe_charge.amount / 100, 2)

        print(intent)

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