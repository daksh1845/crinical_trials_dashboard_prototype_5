from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse  # Add this import
from rest_framework import routers
from trials.api import ClinicalTrialViewSet

router = routers.DefaultRouter()
router.register(r'trials', ClinicalTrialViewSet)

# Simple temporary home view
def home_view(request):
    return HttpResponse("Welcome to the Clinical Trials API. Go to /admin/ or /api/")

urlpatterns = [
    path('', home_view, name='home'),  # Root URL added here
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]