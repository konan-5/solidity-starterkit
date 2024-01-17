from django.contrib import admin

from .models import CftFile, Tender, TenderDetail


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
    )
    search_fields = ("title",)


@admin.register(TenderDetail)
class TenderDetailAdmin(admin.ModelAdmin):
    list_display = (
        "tender_id",
        "tender_submission_deadline_in_days_hours",
        "name_of_contracting_authority",
        "publish_on_behalf_of",
        "participating_bodies",
        "title",
        "cft_ca_unique_id",
        "evaluation_mechanism",
        "description",
        "procurement_type",
        "directive",
        "procedure",
        "cft_involves",
        "cpv_codes",
        "contact_point",
        "award_per_item",
        "inclusion_of_e_auctions",
        "nuts_codes",
        "estimated_value_eur",
        "above_or_below_threshold",
        "time_limit_for_receipt_of_tenders_or_requests_to_participate",
        "deadline_for_dispatching_invitations",
        "end_of_clarification_period",
        "upload_of_documents_within_the_clarifications",
        "tenders_opening_date",
        "allow_suppliers_to_make_an_online_expression_of_interest",
        "contract_awarded_in_lots",
        "contract_duration_in_months_or_years_excluding_extensions",
        "validity_of_tender_in_days_or_months",
        "eu_funding",
        "multiple_tenders_will_be_accepted",
        "date_of_publication_invitation",
        "ted_links_for_published_notices",
        "date_of_awarding",
        "language_of_publication",
        "number_of_openers",
        "cft_file",
    )
    search_fields = ("tender_id",)
