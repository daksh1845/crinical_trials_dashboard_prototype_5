from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse, JsonResponse
from rest_framework import routers
from trials.api import ClinicalTrialViewSet

# Debug views
def home_view(request):
    return HttpResponse("Welcome to the Clinical Trials API. Go to /admin/ or /api/")

def api_test_view(request):
    return JsonResponse({
        "message": "API is working", 
        "available_endpoints": {
            "api_root": "/api/",
            "trials": "/api/trials/",
            "admin": "/admin/"
        }
    })

# API router setup
router = routers.DefaultRouter()
router.register(r'trials', ClinicalTrialViewSet)

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/test/', api_test_view, name='api-test'),
    path('api/auth/', include('rest_framework.urls')),
]