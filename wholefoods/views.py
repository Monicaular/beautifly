import requests
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseServerError


def custom_404_page(request, exception):
    """
    Custom handler for 404 (Page Not Found) errors.
    """
    return render(request, "404.html", status=404)


def custom_500_page(request):
    """
    Custom handler for 500 (Internal Server Error) errors.
    """
    return render(request, "500.html", status=500)


def induce_500_error(request):
    # Intentionally raise an exception to trigger a 500 error
    raise Exception("This is an intentional 500 error for testing purposes.")


def about_us(request):
    """
    Render the 'About Us' page.
    """
    return render(request, "about_us.html")


def privacy_policy(request):
    """
    Render the 'Privacy Policy' page.
    """
    return render(request, "privacy-policy.html")
