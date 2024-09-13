import logging
from pyramid.httpexceptions import HTTPFound

from sqlalchemy import select

from caerp.forms.business.business import get_business_payment_deadline_edit_schema
from caerp.forms.project.business import get_business_edit_schema

from caerp.models.project.business import BusinessPaymentDeadline
from caerp.utils.widgets import (
    POSTButton,
    Link,
)
from caerp.models.task import Invoice
from caerp.views import (
    DeleteView,
    TreeMixin,
    BaseView,
    BaseEditView,
)
from caerp.views.project.routes import (
    PROJECT_ITEM_ROUTE,
)
from caerp.views.business.routes import (
    BUSINESS_ITEM_FILE_ROUTE,
    BUSINESS_ITEM_ROUTE,
    BUSINESS_ITEM_OVERVIEW_ROUTE,
    BUSINESS_ITEM_ESTIMATION_ROUTE,
    BUSINESS_PAYMENT_DEADLINE_ITEM_ROUTE,
)
from caerp.views.project.project import ProjectEntryPointView


logger = logging.getLogger(__name__)


def business_entry_point_view(context, request):
    """
    Project entry point view only redirects to the most appropriate page
    """
    if context.business_type.label == "default":
        last = request.route_path(PROJECT_ITEM_ROUTE, id=context.project_id)
    else:
        last = request.route_path(BUSINESS_ITEM_OVERVIEW_ROUTE, id=context.id)
    return HTTPFound(last)


class BusinessOverviewView(BaseView, TreeMixin):
    """
    Single business view
    """

    route_name = BUSINESS_ITEM_OVERVIEW_ROUTE

    def __init__(self, *args, **kw):
        BaseView.__init__(self, *args, **kw)

    # Relatif au TreeMixin
    @property
    def tree_is_visible(self):
        """
        Check if this node should be displayed in the breadcrumb tree
        """
        if (
            getattr(self.context, "business", None) is not None
            and self.context.business.visible
        ):
            return True
        elif hasattr(self.context, "project"):
            if not self.context.project.project_type.with_business:
                return False
            elif getattr(self.context, "business_id", "other") is None:
                return False
        return True

    @property
    def title(self):
        """
        Return the page title both for the view and for the breadcrumb
        """
        business = self.current()
        if hasattr(self.context, "business"):
            business = self.context.business
        elif hasattr(self.context, "task"):
            business = self.context.task.business

        return "{0.business_type.label} : {0.name}".format(business)

    @property
    def tree_url(self):
        business = self.current()
        return self.request.route_path(self.route_name, id=business.id)

    def current(self):
        business = self.context
        if hasattr(self.context, "business"):
            business = self.context.business
        elif hasattr(self.context, "task"):
            business = self.context.task.business
        return business

    def estimation_add_url(self):
        """
        Build the estimation add url

        :rtype: str
        """
        return self.request.route_path(
            BUSINESS_ITEM_ESTIMATION_ROUTE, id=self.context.id, _query={"action": "add"}
        )

    def estimation_add_link(self):
        """
        Return A POSTButton for adding estimations
        """
        result = None
        if not self.context.closed:
            label = "Devis complémentaire"
            if not self.context.estimations:
                label = "Devis"
            result = POSTButton(
                url=self.estimation_add_url(),
                label=label,
                title=f"Créer un {label}",
                icon="plus",
            )
        return result

    def switch_invoicing_mode_link(self):
        """
        Build a link used to initialize the business invoicing mode
        """
        result = None
        # Seul les affaires sans factures et avec le droit de faire des études
        # de prix
        if (
            not self.context.invoices
            and self.context.project.project_type.include_price_study
        ):
            url = self.request.route_path(
                BUSINESS_ITEM_ROUTE,
                id=self.context.id,
                _query={"action": "switch_mode"},
            )
            if self.context.invoicing_mode == self.context.CLASSIC_MODE:
                label = "Passer à la facturation à l'avancement"
                description = "Utiliser le mode de facturation à l'avancement"
                icon = "steps"
            else:
                label = "Annuler la facturation à l'avancement"
                description = "Revenir à un mode de facturation 'classique'"
                icon = "times"
            result = POSTButton(
                label=label,
                url=url,
                icon=icon,
                title=description,
            )
        return result

    def _get_file_tab_link(self):
        return Link(
            self.request.route_path(BUSINESS_ITEM_FILE_ROUTE, id=self.context.id),
            "",
            title="Voir le détail des fichiers",
            icon="arrow-right",
            css="btn icon only",
        )

    def __call__(self):
        """
        Return the context used in the template

        - Invoicing links
        - Deadlines
        - Add estimation link
        - Indicators
        - File requirements
        """
        self.populate_navigation()
        result = dict(
            title=self.title,
            edit_url=self.request.route_path(
                self.route_name, id=self.context.id, _query={"action": "edit"}
            ),
            switch_invoicing_mode_link=self.switch_invoicing_mode_link(),
            estimations=self.context.estimations,
            custom_indicators=self.context.indicators,
            file_requirements=self.context.get_file_requirements(scoped=False),
            estimation_add_link=self.estimation_add_link(),
            file_tab_link=self._get_file_tab_link(),
        )
        return result


class BusinessEditView(BaseEditView, TreeMixin):
    schema = get_business_edit_schema()
    route_name = BUSINESS_ITEM_ROUTE

    @property
    def title(self):
        return "Modification de {0}".format(self.context.name)

    def before(self, form):
        self.populate_navigation()
        return BaseEditView.before(self, form)

    def redirect(self, appstruct):
        return HTTPFound(
            self.request.route_path(BUSINESS_ITEM_ROUTE, id=self.context.id)
        )


class BusinessSwitchInvoicingModeView(BaseView):
    def __call__(self):
        if self.context.project.project_type.include_price_study:
            if self.context.invoicing_mode == self.context.CLASSIC_MODE:
                self.context.set_progress_invoicing_mode()
            else:
                self.context.unset_progress_invoicing_mode()
            self.dbsession.merge(self.context)
        return HTTPFound(
            self.request.route_path(BUSINESS_ITEM_OVERVIEW_ROUTE, id=self.context.id)
        )


class BusinessPaymentDeadlineEditView(BaseEditView):
    factory = BusinessPaymentDeadline
    route_name = BUSINESS_PAYMENT_DEADLINE_ITEM_ROUTE
    title = "Modification de l'échéance de paiement"
    msg = ""

    def schema(self):
        return get_business_payment_deadline_edit_schema(self.request)

    def on_edit(self, appstruct, model):
        if model.invoice_id:
            invoice_valid = (
                self.request.dbsession.execute(
                    select(Invoice.status).where(Invoice.id == model.invoice_id)
                ).scalar()
                == "valid"
            )
            model.invoiced = invoice_valid
        else:
            model.invoiced = False
        return super().on_edit(appstruct, model)

    def redirect(self, appstruct):
        return HTTPFound(
            self.request.route_path(
                BUSINESS_ITEM_OVERVIEW_ROUTE, id=self.context.business_id
            )
        )


class BusinessPaymentDeadlineDeleteView(DeleteView):
    delete_msg = "L'échéance a bien été supprimée"

    def redirect(self):
        return HTTPFound(
            self.request.route_path(
                BUSINESS_ITEM_OVERVIEW_ROUTE, id=self.context.business_id
            )
        )


def close_business_view(context, request):
    """
    View used to close a Business
    """
    context.closed = True
    request.dbsession.merge(context)
    return HTTPFound(request.route_path(BUSINESS_ITEM_ROUTE, id=context.id))


def includeme(config):
    config.add_view(
        business_entry_point_view,
        route_name=BUSINESS_ITEM_ROUTE,
        permission="view.business",
    )
    config.add_tree_view(
        BusinessOverviewView,
        parent=ProjectEntryPointView,
        renderer="caerp:templates/business/overview.mako",
        permission="view.business",
        layout="business",
    )
    config.add_tree_view(
        BusinessEditView,
        parent=BusinessOverviewView,
        renderer="caerp:templates/base/formpage.mako",
        request_param="action=edit",
        permission="edit.business",
        layout="business",
    )
    config.add_view(
        close_business_view,
        route_name=BUSINESS_ITEM_ROUTE,
        request_param="action=close",
        permission="close.business",
        layout="default",
        request_method="POST",
        require_csrf=True,
    )
    config.add_view(
        BusinessSwitchInvoicingModeView,
        route_name=BUSINESS_ITEM_ROUTE,
        request_param="action=switch_mode",
        layout="business",
        permission="edit.business",
        request_method="POST",
        require_csrf=True,
    )

    config.add_tree_view(
        BusinessPaymentDeadlineEditView,
        parent=BusinessOverviewView,
        permission="edit.business_payment_deadline",
        request_param="action=edit",
        renderer="/base/formpage.mako",
    )
    config.add_view(
        BusinessPaymentDeadlineDeleteView,
        route_name=BUSINESS_PAYMENT_DEADLINE_ITEM_ROUTE,
        request_param="action=delete",
        permission="delete.business_payment_deadline",
        request_method="POST",
        require_csrf=True,
    )
