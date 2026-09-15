from django.urls import include, path


urlpatterns = [
    path("api/", include("apps.content.urls")),
    path("api/contact/", include("apps.contact.urls")),
]
