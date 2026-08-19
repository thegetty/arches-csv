from django.db import migrations


MODULE_ID = "f1d16fa5-4558-4742-b162-c8ab54f63363"


def add_csv_etl_module(apps, schema_editor):
    ETLModule = apps.get_model("models", "ETLModule")
    ETLModule.objects.update_or_create(
        etlmoduleid=MODULE_ID,
        defaults={
            "name": "Import Single CSV Plugin",
            "description": "Import a single CSV file using the external arches-nested-tile-csv-importer plugin.",
            "etl_type": "import",
            "component": "views/components/etl_modules/import-single-csv-plugin",
            "componentname": "import-single-csv-plugin",
            "modulename": "import_single_csv_plugin.py",
            "classname": "ImportSingleCsv",
            "config": {
                "bgColor": "#9591ef",
                "circleColor": "#b0adf3",
                "show": True,
            },
            "icon": "fa fa-upload",
            "slug": "import-single-csv-plugin",
            "helpsortorder": 99,
            "helptemplate": "import-single-csv-help",
            "reversible": True,
        },
    )


def remove_csv_etl_module(apps, schema_editor):
    ETLModule = apps.get_model("models", "ETLModule")
    ETLModule.objects.filter(etlmoduleid=MODULE_ID).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("models", "8449_filter_warning_etl_module"),
    ]

    operations = [
        migrations.RunPython(add_csv_etl_module, remove_csv_etl_module),
    ]
