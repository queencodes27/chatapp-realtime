from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

API_PREFIX = "api/v1/"

# Define Swagger API Schema
schema_view = get_schema_view(
    openapi.Info(
        title="REAL TIME CHAT API",
        default_version="v1",
        description="A Real-time chat app backend that leverages the"
        " power of django restfarmework and django channels",
        terms_of_service="",
        contact=openapi.Contact(email=""),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


swagger_urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema_json",
    ),
    re_path(
        r"^docs/$",
        schema_view.with_ui(
            "swagger",
            cache_timeout=0,
        ),
        name="schema_swagger_ui",
    ),
    re_path(
        r"^redoc/$",
        schema_view.with_ui(
            "redoc",
            cache_timeout=0,
        ),
        name="schema_redoc",
    ),
]

api_urlpatterns = [
    path("auth/", include("account.urls")),
    path("chat/", include("chat.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path(API_PREFIX, include(api_urlpatterns)),
]

urlpatterns += swagger_urlpatterns
