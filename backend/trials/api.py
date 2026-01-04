from rest_framework import viewsets
from .models import ClinicalTrial
from .serializers import ClinicalTrialSerializer

class ClinicalTrialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ClinicalTrial.objects.all()
    serializer_class = ClinicalTrialSerializer