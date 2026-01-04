import csv
from django.core.management.base import BaseCommand
from trials.models import ClinicalTrial

class Command(BaseCommand):
    help = 'Imports clinical trial data from a CSV file, skips duplicates'

    def handle(self, *args, **options):
        csv_file_path = 'cancer_trials.csv'

        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Use get() with fallback to handle missing columns
                ClinicalTrial.objects.update_or_create(
                    trial_id=row['CTRI_No'],
                    defaults={
                        'title': row.get('Public_Title', ''),
                        'type_of_trial': row.get('Type_of_Trial', ''),
                        'recruitment_status': row.get('Recruitment_Status', ''),
                        'health_condition': row.get('Health_Condition', ''),
                        'intervention_name': row.get('Intervention_Name', ''),
                        'locations': row.get('Location', ''),
                    }
                )

        self.stdout.write(self.style.SUCCESS('Data import/update complete'))