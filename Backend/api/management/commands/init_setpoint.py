from django.core.management.base import BaseCommand
from api.models import TemperatureSetpoint


class Command(BaseCommand):
    help = 'Initialize the default temperature setpoint'

    def handle(self, *args, **options):
        setpoint, created = TemperatureSetpoint.objects.get_or_create(
            id=1,
            defaults={
                'setpoint': 25.0,
                'min_setpoint': 15.0,
                'max_setpoint': 40.0,
            }
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created default setpoint: {setpoint.setpoint}°C'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'Setpoint already exists: {setpoint.setpoint}°C'
                )
            )
