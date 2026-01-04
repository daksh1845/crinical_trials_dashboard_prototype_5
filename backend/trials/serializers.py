from rest_framework import serializers
from .models import ClinicalTrial

class ClinicalTrialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalTrial
        fields = '__all__'