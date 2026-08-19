import logging
from celery import shared_task
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from arches.app.models import models
from arches.app.tasks import notify_completion

@shared_task
def load_single_csv(
    userid,
    loadid,
    graphid,
    has_headers,
    fieldnames,
    csv_mapping,
    csv_file_name,
    id_label,
    updatevalue
):
    logger = logging.getLogger(__name__)

    try:
        from arches_nested_tile_csv_importer.etl_modules.import_single_csv_plugin import ImportSingleCsv

        import_single_csv = ImportSingleCsv(loadid=loadid)
        import_single_csv.run_load_task(
            userid,
            loadid,
            graphid,
            has_headers,
            fieldnames,
            csv_mapping,
            csv_file_name,
            id_label,
            updatevalue,
        )

        load_event = models.LoadEvent.objects.get(loadid=loadid)
        status = _("Completed") if load_event.status == "indexed" else _("Failed")
    except Exception as e:
        logger.error(e)
        load_event = models.LoadEvent.objects.get(loadid=loadid)
        load_event.status = "failed"
        load_event.save()
        status = _("Failed")
    finally:
        msg = _("Single CSV Import: {} [{}]").format(csv_file_name, status)
        user = User.objects.get(id=userid)
        notify_completion(msg, user)
