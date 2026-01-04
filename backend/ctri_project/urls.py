from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse, JsonResponse
from rest_framework import routers

# Simple test views
def home_view(request):
    return HttpResponse("Welcome to Clinical Trials API. Go to /admin or /api/")

def api_test_view(request):
    return JsonResponse({
        "status": "success",
        "message": "API is working",
        "endpoints": {
            "trials": "/api/trials/",
            "admin": "/admin/",
            "test": "/api/test/"
        }
    })

def trials_view(request):
    return JsonResponse({
        "message": "Trials endpoint placeholder",
        "next_step": "Enable ClinicalTrialViewSet in trials/api.py"
    })

# Create router but don't register yet
router = routers.DefaultRouter()

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/test/', api_test_view, name='api-test'),
    path('api/trials/', trials_view, name='trials-list'),
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
]

# Try to import and register ClinicalTrialViewSet safely
try:
    from trials.api import ClinicalTrialViewSet
    router.register(r'trials', ClinicalTrialViewSet)
    # Add the router URLs
    urlpatterns.append(path('api/', include(router.urls)))
    print("✓ ClinicalTrialViewSet registered successfully")
except ImportError as e:
    print(f"✗ Could not import ClinicalTrialViewSet: {e}")
except Exception as e:
    print(f"✗ Error registering ClinicalTrialViewSet: {e}")