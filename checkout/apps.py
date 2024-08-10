from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    """Configuration for the Checkout app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "checkout"

    def ready(self):
        """Import signals for the Checkout app."""

        import checkout.signals
