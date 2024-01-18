from django.db import models

from tendr_backend.common.models import Common


class CftFile(Common):
    addendum_id = models.CharField(null=True, blank=True, max_length=2048)
    title = models.CharField(null=True, blank=True, max_length=2048)
    file = models.FileField(upload_to="cft_file/", null=True, blank=True)
    description = models.CharField(null=True, blank=True, max_length=2048)
    lang = models.CharField(null=True, blank=True, max_length=2048)
    doument_version = models.CharField(null=True, blank=True, max_length=2048)
    action = models.CharField(null=True, blank=True, max_length=2048)


class Tender(Common):
    title = models.CharField(null=True, blank=True, max_length=2048)
    resource_id = models.CharField(max_length=2048, unique=True)
    ca = models.CharField(null=True, blank=True, max_length=2048)
    info = models.TextField(null=True, blank=True)
    date_published = models.CharField(null=True, blank=True, max_length=2048)
    tenders_submission_deadline = models.CharField(null=True, blank=True, max_length=2048)
    procedure = models.CharField(null=True, blank=True, max_length=2048)
    status = models.CharField(null=True, blank=True, max_length=2048)
    notice_pdf = models.FileField(null=True, blank=True, upload_to="notice_pdf/")
    award_date = models.CharField(null=True, blank=True, max_length=2048)
    estimated_value = models.CharField(null=True, blank=True, max_length=2048)
    cycle = models.CharField(null=True, blank=True, max_length=2048)
    tender_detail = models.JSONField(default=dict, null=True, blank=True)
    cft_file = models.ManyToManyField(CftFile)

    def __str__(self):
        return f"{self.title}"  # noqa
