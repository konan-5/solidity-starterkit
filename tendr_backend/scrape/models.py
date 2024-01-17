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
    resource_id = models.CharField(null=True, blank=True, max_length=2048)
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

    def __str__(self):
        return f"{self.title}"  # noqa


class TenderDetail(Common):
    tender_id = models.ForeignKey(Tender, on_delete=models.CASCADE)
    tender_submission_deadline_in_days_hours = models.CharField(null=True, blank=True, max_length=2048)
    name_of_contracting_authority = models.CharField(null=True, blank=True, max_length=2048)
    publish_on_behalf_of = models.CharField(null=True, blank=True, max_length=2048)
    participating_bodies = models.CharField(null=True, blank=True, max_length=2048)
    title = models.CharField(null=True, blank=True, max_length=2048)
    cft_ca_unique_id = models.CharField(null=True, blank=True, max_length=2048)
    evaluation_mechanism = models.CharField(null=True, blank=True, max_length=2048)
    description = models.TextField(null=True, blank=True)
    procurement_type = models.CharField(null=True, blank=True, max_length=2048)
    directive = models.CharField(null=True, blank=True, max_length=2048)
    procedure = models.CharField(null=True, blank=True, max_length=2048)
    cft_involves = models.CharField(null=True, blank=True, max_length=2048)
    cpv_codes = models.CharField(null=True, blank=True, max_length=2048)
    contact_point = models.CharField(null=True, blank=True, max_length=2048)
    award_per_item = models.CharField(null=True, blank=True, max_length=2048)
    inclusion_of_e_auctions = models.CharField(null=True, blank=True, max_length=2048)
    nuts_codes = models.CharField(null=True, blank=True, max_length=2048)
    estimated_value_eur = models.CharField(null=True, blank=True, max_length=2048)
    above_or_below_threshold = models.CharField(null=True, blank=True, max_length=2048)
    time_limit_for_receipt_of_tenders_or_requests_to_participate = models.CharField(
        null=True, blank=True, max_length=2048
    )
    deadline_for_dispatching_invitations = models.CharField(null=True, blank=True, max_length=2048)
    end_of_clarification_period = models.CharField(null=True, blank=True, max_length=2048)
    upload_of_documents_within_the_clarifications = models.CharField(null=True, blank=True, max_length=2048)
    tenders_opening_date = models.CharField(null=True, blank=True, max_length=2048)
    allow_suppliers_to_make_an_online_expression_of_interest = models.CharField(null=True, blank=True, max_length=2048)
    contract_awarded_in_lots = models.CharField(null=True, blank=True, max_length=2048)
    contract_duration_in_months_or_years_excluding_extensions = models.CharField(
        null=True, blank=True, max_length=2048
    )
    validity_of_tender_in_days_or_months = models.CharField(null=True, blank=True, max_length=2048)
    eu_funding = models.CharField(null=True, blank=True, max_length=2048)
    multiple_tenders_will_be_accepted = models.CharField(null=True, blank=True, max_length=2048)
    date_of_publication_invitation = models.CharField(null=True, blank=True, max_length=2048)
    ted_links_for_published_notices = models.CharField(null=True, blank=True, max_length=2048)
    date_of_awarding = models.CharField(null=True, blank=True, max_length=2048)
    language_of_publication = models.CharField(null=True, blank=True, max_length=2048)
    number_of_openers = models.CharField(null=True, blank=True, max_length=2048)
    cft_file = models.ManyToManyField(CftFile)

    def __str__(self):
        return f"{self.tender_id.title}"
