"""
    View for assets
"""
import os
import logging

from pyramid.httpexceptions import HTTPFound

from caerp.utils.datetimes import format_date

from caerp.utils.widgets import (
    ViewLink,
)

from caerp.models.task import (
    CancelInvoice,
)

from caerp.resources import (
    task_preview_css,
)

from caerp.forms.tasks.invoice import get_add_edit_cancelinvoice_schema

from caerp.views import (
    BaseEditView,
    add_panel_page_view,
)
from caerp.views.business.business import BusinessOverviewView

from caerp.views.task.utils import get_task_url
from caerp.views.task.views import (
    TaskEditView,
    TaskPdfView,
    TaskSetMetadatasView,
    TaskSetProductsView,
    TaskSetDraftView,
    TaskMoveToPhaseView,
    TaskGeneralView,
    TaskPreviewView,
    TaskFilesView,
    TaskFileUploadView,
)
from .routes import (
    CINV_ITEM_ROUTE,
    CINV_ITEM_GENERAL_ROUTE,
    CINV_ITEM_PREVIEW_ROUTE,
    CINV_ITEM_ACCOUNTING_ROUTE,
    CINV_ITEM_FILES_ROUTE,
)
from .invoice import InvoiceDeleteView, InvoiceAccountingView


log = logging.getLogger(__name__)


class CancelInvoiceEditView(TaskEditView):
    route_name = "/cancelinvoices/{id}"

    @property
    def title(self):
        customer = self.context.customer
        customer_label = customer.label
        if customer.code is not None:
            customer_label += " ({0})".format(customer.code)

        return (
            "Modification de l’{tasktype_label} « {task.name} » "
            "avec le client {customer}".format(
                task=self.context,
                customer=customer_label,
                tasktype_label=self.context.get_type_label().lower(),
            )
        )

    def get_js_app_options(self) -> dict:
        options = super().get_js_app_options()
        options.update(
            {
                "invoicing_mode": self.context.invoicing_mode,
            }
        )
        return options


class CancelInvoiceDeleteView(InvoiceDeleteView):
    msg = "L'avoir {context.name} a bien été supprimé."


# VUE pour les factures validées
def get_title(invoice):
    return "Avoir numéro {0}".format(invoice.official_number)


class CancelInvoiceGeneralView(TaskGeneralView):
    route_name = CINV_ITEM_GENERAL_ROUTE
    file_route_name = CINV_ITEM_FILES_ROUTE

    @property
    def title(self):
        return get_title(self.current())


class CancelInvoicePreviewView(TaskPreviewView):
    route_name = CINV_ITEM_PREVIEW_ROUTE

    @property
    def title(self):
        return get_title(self.current())


class CancelInvoiceAccountingView(InvoiceAccountingView):
    route_name = CINV_ITEM_ACCOUNTING_ROUTE

    @property
    def title(self):
        return get_title(self.current())


class CancelInvoiceFilesView(TaskFilesView):
    route_name = CINV_ITEM_FILES_ROUTE

    @property
    def title(self):
        return get_title(self.current())


class CancelInvoicePdfView(TaskPdfView):
    pass


class CancelInvoiceAdminView(BaseEditView):
    factory = CancelInvoice
    schema = get_add_edit_cancelinvoice_schema(isadmin=True)


class CancelInvoiceSetTreasuryiew(BaseEditView):
    """
    View used to set treasury related informations

    context

        An invoice

    perms

        set_treasury.invoice
    """

    factory = CancelInvoice
    schema = get_add_edit_cancelinvoice_schema(
        includes=("financial_year",),
        title="Modifier l'année fiscale de la facture d'avoir",
    )

    def redirect(self, appstruct):
        return HTTPFound(
            get_task_url(self.request, suffix="/accounting"),
        )

    def before(self, form):
        BaseEditView.before(self, form)
        self.request.actionmenu.add(
            ViewLink(
                label="Revenir à la facture",
                url=get_task_url(self.request, suffix="/accounting"),
            )
        )

    @property
    def title(self):
        return "Avoir numéro {0} en date du {1}".format(
            self.context.official_number,
            format_date(self.context.date),
        )


class CancelInvoiceSetMetadatasView(TaskSetMetadatasView):
    """
    View used for editing invoice metadatas
    """

    @property
    def title(self):
        return "Modification de l’{tasktype_label} {task.name}".format(
            task=self.context,
            tasktype_label=self.context.get_type_label().lower(),
        )


class CancelInvoiceSetProductsView(TaskSetProductsView):
    @property
    def title(self):
        return "Configuration des codes produits pour l’avoir {0.name}".format(
            self.context
        )


def add_routes(config):
    """
    Add module related routes
    """
    for extension in ("html", "pdf", "preview"):
        route = f"{CINV_ITEM_ROUTE}.{extension}"
        config.add_route(route, route, traverse="/tasks/{id}")

    for action in (
        "addfile",
        "delete",
        "admin",
        "set_treasury",
        "set_products",
        "set_metadatas",
        "set_draft",
        "move",
    ):
        route = os.path.join(CINV_ITEM_ROUTE, action)
        config.add_route(route, route, traverse="/tasks/{id}")


def includeme(config):
    add_routes(config)

    # Here it's only view.cancelinvoice to allow redirection to the html view
    config.add_tree_view(
        CancelInvoiceEditView,
        parent=BusinessOverviewView,
        renderer="tasks/form.mako",
        permission="view.cancelinvoice",
        context=CancelInvoice,
    )

    config.add_view(
        CancelInvoiceAdminView,
        route_name="/cancelinvoices/{id}/admin",
        renderer="base/formpage.mako",
        request_param="token=admin",
        permission="admin",
        context=CancelInvoice,
    )

    config.add_view(
        CancelInvoiceDeleteView,
        route_name="/cancelinvoices/{id}/delete",
        permission="delete.cancelinvoice",
        require_csrf=True,
        request_method="POST",
        context=CancelInvoice,
    )

    config.add_view(
        CancelInvoicePdfView,
        route_name="/cancelinvoices/{id}.pdf",
        permission="view.cancelinvoice",
        context=CancelInvoice,
    )

    add_panel_page_view(
        config,
        "task_pdf_content",
        js_resources=(task_preview_css,),
        route_name="/cancelinvoices/{id}.preview",
        permission="view.cancelinvoice",
        context=CancelInvoice,
    )

    config.add_view(
        TaskFileUploadView,
        route_name="/cancelinvoices/{id}/addfile",
        renderer="base/formpage.mako",
        permission="add.file",
        context=CancelInvoice,
    )

    config.add_view(
        CancelInvoiceSetTreasuryiew,
        route_name="/cancelinvoices/{id}/set_treasury",
        renderer="base/formpage.mako",
        permission="set_treasury.cancelinvoice",
        context=CancelInvoice,
    )
    config.add_view(
        CancelInvoiceSetMetadatasView,
        route_name="/cancelinvoices/{id}/set_metadatas",
        renderer="tasks/duplicate.mako",
        permission="view.cancelinvoice",
        context=CancelInvoice,
    )
    config.add_view(
        TaskSetDraftView,
        route_name="/cancelinvoices/{id}/set_draft",
        permission="draft.cancelinvoice",
        require_csrf=True,
        request_method="POST",
        context=CancelInvoice,
    )
    config.add_view(
        CancelInvoiceSetProductsView,
        route_name="/cancelinvoices/{id}/set_products",
        permission="set_treasury.cancelinvoice",
        renderer="base/formpage.mako",
        context=CancelInvoice,
    )
    config.add_view(
        TaskMoveToPhaseView,
        route_name="/cancelinvoices/{id}/move",
        permission="view.cancelinvoice",
        require_csrf=True,
        request_method="POST",
        context=CancelInvoice,
    )

    config.add_tree_view(
        CancelInvoiceGeneralView,
        parent=BusinessOverviewView,
        layout="cancelinvoice",
        renderer="tasks/cancelinvoice/general.mako",
        permission="view.node",
        context=CancelInvoice,
    )
    config.add_tree_view(
        CancelInvoicePreviewView,
        parent=BusinessOverviewView,
        layout="cancelinvoice",
        renderer="tasks/preview.mako",
        permission="view.node",
        context=CancelInvoice,
    )
    config.add_tree_view(
        CancelInvoiceAccountingView,
        parent=BusinessOverviewView,
        layout="cancelinvoice",
        renderer="tasks/cancelinvoice/accounting.mako",
        permission="view.node",
        context=CancelInvoice,
    )
    config.add_tree_view(
        CancelInvoiceFilesView,
        parent=BusinessOverviewView,
        layout="cancelinvoice",
        renderer="tasks/files.mako",
        permission="view.node",
        context=CancelInvoice,
    )
