from caerp_base.models.base import DBSESSION
from caerp.plugins.sap_urssaf3p.forms.tasks.invoice import get_urssaf3p_list_schema
from caerp.models.task import Task
from caerp.plugins.sap_urssaf3p.models import URSSAFPaymentRequest
from caerp.views.invoices.lists import (
    GlobalInvoicesListView,
    CompanyInvoicesListView,
)
from caerp.views.invoices.routes import INVOICE_COLLECTION_ROUTE
from caerp.views.company.routes import COMPANY_INVOICES_ROUTE


def filter_invoices_by_urssaf3p_request_status(query, appstruct):
    """
    Filter invoices by urssaf3p request status
    """
    urssaf3p_request_status = appstruct.get("avance_immediate")
    if urssaf3p_request_status not in ("all", None):
        subquery = (
            DBSESSION()
            .query(URSSAFPaymentRequest)
            .filter(URSSAFPaymentRequest.parent_id == Task.id)
        )
        if urssaf3p_request_status != "requested":
            subquery = subquery.filter(
                URSSAFPaymentRequest.request_status == urssaf3p_request_status
            )
        query = query.filter(subquery.exists())
    return query


class URSSAF3PGlobalInvoicesListView(GlobalInvoicesListView):
    schema = get_urssaf3p_list_schema(is_global=True, excludes=("status",))

    def filter_avance_immediate(self, query, appstruct):
        return filter_invoices_by_urssaf3p_request_status(query, appstruct)


class URSSAF3PCompanyInvoicesListView(CompanyInvoicesListView):
    schema = get_urssaf3p_list_schema(
        is_global=False,
        excludes=("company_id", "validator_id", "auto_validated"),
    )

    def filter_avance_immediate(self, query, appstruct):
        return filter_invoices_by_urssaf3p_request_status(query, appstruct)


def includeme(config):
    config.add_view(
        URSSAF3PGlobalInvoicesListView,
        route_name=INVOICE_COLLECTION_ROUTE,
        renderer="invoices.mako",
        permission="admin.invoices",
    )
    config.add_view(
        URSSAF3PCompanyInvoicesListView,
        route_name=COMPANY_INVOICES_ROUTE,
        renderer="invoices.mako",
        permission="list_invoices",
    )
