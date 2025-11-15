from django.db import migrations

def forwards(apps, schema_editor):
    VehicleType = apps.get_model('core', 'VehicleType')
    ProductSpec = apps.get_model('core', 'ProductSpec')

    for spec in ProductSpec.objects.all():
        codes = spec.vehicle_types or []
        for code in codes:
            vt, created = VehicleType.objects.get_or_create(
                code=code,
                defaults={'name': code}
            )
            spec.vehicle_types_rel.add(vt)

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_vehicletype_productspec_vehicle_types_rel'),
    ]

    operations = [
        migrations.RunPython(forwards),
    ]
