import json

from django.http import JsonResponse
from django.urls import path


def submit_inquiry(request):
    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"detail": "Invalid JSON"}, status=400)

    errors = {
        field: "This field is required."
        for field in ("name", "email", "message")
        if not str(payload.get(field, "")).strip()
    }
    if errors:
        return JsonResponse({"errors": errors}, status=400)

    return JsonResponse(
        {"detail": "Your inquiry has been received."}, status=202
    )


urlpatterns = [path("", submit_inquiry, name="submit-inquiry")]
