from django.conf import settings

BULK_EXPORT_DIR = getattr(settings, 'BULK_EXPORT_DIR', '/files/')

TASK_NOT_FOUND   = -1
TASK_NEW         = 0
TASK_RUNNING     = 1
TASK_SUCCESSFUL  = 2
TASK_ABORTED     = 3
TASK_UNKNOWN     = 4
TASK_FAILED      = 5

STATUS_CHOICES = (
        (TASK_NEW, 'New'),
        (TASK_RUNNING, 'Running'),
        (TASK_SUCCESSFUL, 'Successful'),
        (TASK_ABORTED, 'Aborted'),
        (TASK_FAILED, 'Failed')
    )
