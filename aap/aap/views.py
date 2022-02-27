"""AAP views."""
from django.http import JsonResponse


def health_check(request):
    """AAP health check."""
    return JsonResponse({"status": "ok"})
