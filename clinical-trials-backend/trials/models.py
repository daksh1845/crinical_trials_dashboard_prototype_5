from django.db import models  # ADD THIS LINE

class ClinicalTrial(models.Model):
    trial_id = models.CharField(max_length=100, unique=True)
    title = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)
    type_of_trial = models.CharField(max_length=100, blank=True)
    recruitment_status = models.CharField(max_length=100, blank=True)
    health_condition = models.TextField(blank=True)
    intervention_name = models.TextField(blank=True)
    locations = models.TextField(blank=True)