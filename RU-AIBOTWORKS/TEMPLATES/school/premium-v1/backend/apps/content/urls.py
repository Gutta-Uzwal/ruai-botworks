from django.http import JsonResponse
from django.urls import path


def published_content(request):
    if request.method != "GET":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    return JsonResponse(
        {
            "site": {"name": "School", "tagline": "Learning with purpose."},
            "navigation": [
                {"label": "About", "href": "/about"},
                {"label": "Admissions", "href": "/admissions"},
                {"label": "Academics", "href": "/academics"},
                {"label": "Campus life", "href": "/campus-life"},
                {"label": "Contact", "href": "/contact"},
            ],
            "updates": [],
        }
    )


urlpatterns = [path("content/", published_content, name="published-content")]
