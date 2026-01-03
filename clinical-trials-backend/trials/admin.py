from django.contrib import admin
from .models import ClinicalTrial

class ClinicalTrialAdmin(admin.ModelAdmin):
    list_display = ('trial_id', 'title', 'recruitment_status', 'health_condition', 'last_updated')
    list_filter = ('recruitment_status', 'type_of_trial')
    search_fields = ('trial_id', 'title', 'health_condition')
    # Optional: Add more fields to list_display if you want
    list_display = ('trial_id', 'title', 'type_of_trial', 'recruitment_status', 'health_condition', 'intervention_name', 'locations')

admin.site.register(ClinicalTrial, ClinicalTrialAdmin)