from django.contrib import admin
from django.urls import path, include

from apps.users.urls import urlpatterns as user_urlpatterns
from apps.polls.urls import urlpatterns as polls_urlpatterns


api_urlpatterns = [
    *user_urlpatterns,
    *polls_urlpatterns,
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(api_urlpatterns)),
    path("api/docs/", include("docs.urls")),
]

