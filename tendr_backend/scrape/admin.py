from django.contrib import admin

from .models import CftFile, Tender


@admin.register(CftFile)
class CftFileAdmin(admin.ModelAdmin):
    list_display = (
        "addendum_id",
        "title",
        "file",
        "description",
        "lang",
        "doument_version",
        "action",
    )
    search_fields = ("title",)


@admin.register(Tender)
class TenderAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "resource_id",
        "ca",
        "info",
        "date_published",
        "tenders_submission_deadline",
        "procedure",
        "status",
        "notice_pdf",
        "award_date",
        "estimated_value",
        "cycle",
        "tender_detail",
        # "cft_file",
    )
    search_fields = ("title",)
