"""Thrush views."""
from django.http import JsonResponse


def health_check(request):
    """Thrush health check."""
    return JsonResponse({"status": "ok"})
