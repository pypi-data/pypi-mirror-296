import logging

from caerp.models.task import Task
from caerp.forms.tasks.invoice import get_list_schema
from caerp.views import TreeMixin
from caerp.views.company.routes import COMPANY_INVOICE_ADD_ROUTE
from caerp.views.invoices.lists import (
    CompanyInvoicesListView,
    CompanyInvoicesCsvView,
    CompanyInvoicesXlsView,
    CompanyInvoicesOdsView,
    filter_all_status,
)
from caerp.views.project.project import (
    ProjectListView,
)
from caerp.views.project.routes import (
    PROJECT_ITEM_INVOICE_ROUTE,
    PROJECT_ITEM_INVOICE_EXPORT_ROUTE,
)


logger = logging.getLogger(__name__)


class ProjectInvoiceListView(CompanyInvoicesListView, TreeMixin):
    """
    Invoice list for one given company
    """

    route_name = PROJECT_ITEM_INVOICE_ROUTE
    schema = get_list_schema(
        is_global=False,
        excludes=(
            "company_id",
            "financial_year",
        ),
    )
    add_template_vars = CompanyInvoicesListView.add_template_vars + ("add_url",)
    is_admin = False

    @property
    def add_url(self):
        return self.request.route_path(
            COMPANY_INVOICE_ADD_ROUTE,
            id=self.context.company_id,
            _query={"project_id": self.context.id},
        )

    def _get_company_id(self, appstruct):
        return self.request.context.company_id

    @property
    def title(self):
        return "Factures du dossier {0}".format(self.request.context.name)

    def filter_project(self, query, appstruct):
        self.populate_navigation()
        query = query.filter(Task.project_id == self.context.id)
        return query


class ProjectInvoicesCsvView(CompanyInvoicesCsvView):
    schema = get_list_schema(
        is_global=False,
        excludes=(
            "company_id",
            "financial_year",
        ),
    )

    def _get_company_id(self, appstruct):
        return self.request.context.company_id

    def filter_project(self, query, appstruct):
        logger.debug(" + Filtering by project_id")
        return query.filter(Task.project_id == self.context.id)

    filter_status = filter_all_status


class ProjectInvoicesXlsView(CompanyInvoicesXlsView):
    schema = get_list_schema(
        is_global=False,
        excludes=(
            "company_id",
            "financial_year",
        ),
    )

    def _get_company_id(self, appstruct):
        return self.request.context.company_id

    def filter_project(self, query, appstruct):
        logger.debug(" + Filtering by project_id")
        return query.filter(Task.project_id == self.context.id)

    filter_status = filter_all_status


class ProjectInvoicesOdsView(CompanyInvoicesOdsView):
    schema = get_list_schema(
        is_global=False,
        excludes=(
            "company_id",
            "financial_year",
        ),
    )

    def _get_company_id(self, appstruct):
        return self.request.context.company_id

    def filter_project(self, query, appstruct):
        logger.debug(" + Filtering by project_id")
        return query.filter(Task.project_id == self.context.id)

    filter_status = filter_all_status


def includeme(config):
    config.add_tree_view(
        ProjectInvoiceListView,
        parent=ProjectListView,
        renderer="project/invoices.mako",
        permission="list_invoices",
        layout="project",
    )
    config.add_view(
        ProjectInvoicesCsvView,
        route_name=PROJECT_ITEM_INVOICE_EXPORT_ROUTE,
        match_param="extension=csv",
        permission="list_invoices",
    )

    config.add_view(
        ProjectInvoicesOdsView,
        route_name=PROJECT_ITEM_INVOICE_EXPORT_ROUTE,
        match_param="extension=ods",
        permission="list_invoices",
    )

    config.add_view(
        ProjectInvoicesXlsView,
        route_name=PROJECT_ITEM_INVOICE_EXPORT_ROUTE,
        match_param="extension=xls",
        permission="list_invoices",
    )
