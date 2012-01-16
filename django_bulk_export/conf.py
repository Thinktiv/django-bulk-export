from django.conf import settings

BULK_EXPORT_DIR = getattr(settings, 'BULK_EXPORT_DIR', '/files/')