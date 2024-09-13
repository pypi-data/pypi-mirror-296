import logging
from typing import Dict

from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPFound
from deform_extensions import GridFormWidget

from caerp.resources import node_view_only_js
from caerp.models.third_party.supplier import Supplier
from caerp.utils.widgets import (
    Link,
    ViewLink,
    POSTButton,
)
from caerp.utils.rest import make_redirect_view
from caerp.forms.third_party.supplier import (
    get_supplier_schema,
    get_edit_internal_supplier_schema,
)
from caerp.views import (
    BaseFormView,
    submit_btn,
    cancel_btn,
    JsAppViewMixin,
)
from caerp.views.csv_import import (
    CsvFileUploadView,
    ConfigFieldAssociationView,
)
from .base import (
    SUPPLIER_FORM_GRID,
)

logger = log = logging.getLogger(__name__)


def supplier_archive(request):
    """
    Archive the current supplier
    """
    supplier = request.context
    if not supplier.archived:
        supplier.archived = True
    else:
        supplier.archived = False
    request.dbsession.merge(supplier)
    return HTTPFound(request.referer)


def supplier_delete(request):
    """
    Delete the current supplier
    """
    supplier = request.context
    request.dbsession.delete(supplier)
    request.session.flash(
        "Le fournisseur '{0}' a bien été supprimé".format(supplier.label)
    )
    return HTTPFound(request.referer)


class BaseSupplierView(BaseFormView, JsAppViewMixin):
    """
    Return the view of a supplier
    """

    def _get_more_actions(self):
        """
        Collect available buttons that will be displayed in the upper left
        corner of the screen

        :rtype: list
        """
        return [
            Link(
                self.request.route_path(
                    "supplier", id=self.context.id, _query=dict(action="edit")
                ),
                "Modifier",
                icon="pen",
                css="btn icon only",
            ),
        ]

    def _get_main_actions(self):
        """
        Collect available buttons that will be displayed in the upper right
        corner of the screen

        :rtype: list
        """
        result = []
        pending_orders = self.context.get_orders(
            pending_invoice_only=True, internal=False
        )
        pending_orders_ids = [i.id for i in pending_orders]

        if pending_orders_ids:
            result.append(
                POSTButton(
                    self.request.route_path(
                        "/companies/{id}/supplier_invoices",
                        id=self.context.company_id,
                        _query=dict(action="new"),
                    ),
                    'Facturer<span class="no_mobile">&nbsp;les encours validés'
                    "</span>",
                    icon="file-invoice-euro",
                    css="btn btn-primary icon",
                    extra_fields=[
                        ("supplier_orders_ids", pending_orders_ids),
                        ("submit", ""),
                    ],
                    title="Facturer les encours validés",
                )
            )
        if not self.context.is_internal():
            result.append(
                POSTButton(
                    self.request.route_path(
                        "/companies/{id}/supplier_orders",
                        id=self.context.company_id,
                        _query=dict(action="new"),
                    ),
                    '<span class="screen-reader-text">Nouvelle </span>' "Commande",
                    icon="plus",
                    css="btn btn-primary icon",
                    extra_fields=[
                        ("supplier_id", self.context.id),
                        ("submit", ""),
                    ],
                    title="Nouvelle commande",
                )
            )
            result.append(
                POSTButton(
                    self.request.route_path(
                        "/companies/{id}/supplier_invoices",
                        id=self.context.company_id,
                        _query=dict(action="new"),
                    ),
                    '<span class="screen-reader-text">Nouvelle </span>' "Facture",
                    icon="plus",
                    css="btn icon",
                    extra_fields=[
                        ("supplier_id", self.context.id),
                        ("submit", ""),
                    ],
                    title="Nouvelle facture",
                )
            )
        return result

    def context_url(self, _query: Dict[str, str] = {}):
        return self.request.route_url(
            "/api/v1/suppliers/{id}", id=self.context.id, _query=_query
        )

    def __call__(self):
        populate_actionmenu(self.request)
        node_view_only_js.need()
        title = "Fournisseur : {0}".format(self.context.label)
        if self.request.context.code:
            title += " - {0}".format(self.context.code)

        return dict(
            title=title,
            supplier=self.request.context,
            main_actions=self._get_main_actions(),
            more_actions=self._get_more_actions(),
            records=self.get_subview_records(),
            js_app_options=self.get_js_app_options(),
        )

    def get_subview_records(self):
        """
        Returns a list of items to show additionaly to the main view.
        """
        raise NotImplementedError()


class SupplierViewRunningOrders(BaseSupplierView):
    """Supplier detail with running orders tab opened"""

    def get_subview_records(self):
        from caerp.models.supply import SupplierOrder

        query = self.context.get_orders(waiting_only=True)
        query = query.order_by(-SupplierOrder.created_at)
        return query


class SupplierViewInvoicedOrders(BaseSupplierView):
    """Supplier detail with invoiced orders tab opened"""

    def get_subview_records(self):
        from caerp.models.supply import SupplierOrder

        query = self.context.get_orders(invoiced_only=True)
        query = query.order_by(-SupplierOrder.created_at)
        return query


class SupplierViewExpenseLines(BaseSupplierView):
    def get_subview_records(self):
        query = self.context.get_expenselines()
        return query


class SupplierViewInvoices(BaseSupplierView):
    """Supplier detail with invoices tab opened"""

    def get_subview_records(self):
        from caerp.models.supply import SupplierInvoice

        query = self.context.get_invoices()
        query = query.order_by(-SupplierInvoice.date)
        return query


class SupplierAdd(BaseFormView):
    """
    Supplier add form
    """

    add_template_vars = (
        "title",
        "suppliers",
    )
    title = "Ajouter un fournisseur"
    _schema = None
    buttons = (submit_btn, cancel_btn)
    validation_msg = "Le fournisseur a bien été ajouté"

    @property
    def form_options(self):
        return (("formid", "supplier"),)

    @property
    def suppliers(self):
        codes = self.context.get_supplier_codes_and_names()
        return codes

    # Schema is here a property since we need to build it dynamically regarding
    # the current request (the same should have been built using the after_bind
    # method ?)
    @property
    def schema(self):
        """
        The getter for our schema property
        """
        if self._schema is None:
            self._schema = get_supplier_schema()
        return self._schema

    @schema.setter
    def schema(self, value):
        """
        A setter for the schema property
        The BaseClass in pyramid_deform gets and sets the schema attribute that
        is here transformed as a property
        """
        self._schema = value

    def before(self, form):
        populate_actionmenu(self.request, self.context)
        form.widget = GridFormWidget(named_grid=SUPPLIER_FORM_GRID)

    def submit_success(self, appstruct):
        model = self.schema.objectify(appstruct)
        model.company = self.context
        model.type = "company"
        self.dbsession.add(model)
        self.dbsession.flush()
        self.session.flash(self.validation_msg)
        return HTTPFound(self.request.route_path("supplier", id=model.id))

    def cancel_success(self, appstruct):
        return HTTPFound(
            self.request.route_path("company_suppliers", id=self.context.id)
        )

    cancel_failure = cancel_success


class SupplierEdit(SupplierAdd):
    """
    Supplier edition form
    """

    add_template_vars = (
        "title",
        "suppliers",
    )
    validation_msg = "Le fournisseur a été modifié avec succès"

    @property
    def schema(self):
        """
        The getter for our schema property
        """
        if self._schema is None:
            if self.context.is_internal():
                self._schema = get_edit_internal_supplier_schema()
            else:
                self._schema = get_supplier_schema()
        return self._schema

    @schema.setter
    def schema(self, value):
        """
        A setter for the schema property
        The BaseClass in pyramid_deform gets and sets the schema attribute that
        is here transformed as a property
        """
        self._schema = value

    def appstruct(self):
        """
        Populate the form with the current edited context (supplier)
        """
        return self.schema.dictify(self.request.context)

    @reify
    def title(self):
        return "Modifier le fournisseur '{0}'".format(self.request.context.company_name)

    @property
    def suppliers(self):
        company = self.context.company
        codes = company.get_supplier_codes_and_names()
        codes.filter(Supplier.id != self.context.id)
        return codes

    def submit_success(self, appstruct):
        model = self.schema.objectify(appstruct, self.context)
        model = self.dbsession.merge(model)
        self.dbsession.flush()
        self.session.flash(self.validation_msg)
        come_from = self.request.params.get("come_from", None)
        if come_from:
            return HTTPFound(come_from)
        else:
            return HTTPFound(self.request.route_path("supplier", id=model.id))

    def cancel_success(self, appstruct):
        return HTTPFound(self.request.route_path("supplier", id=self.context.id))


def populate_actionmenu(request, context=None):
    """
    populate the actionmenu for the different views (list/add/edit ...)
    """
    company_id = request.context.get_company_id()
    request.actionmenu.add(get_list_view_btn(company_id))
    if context is not None and context.__name__ == "supplier":
        request.actionmenu.add(get_view_btn(context.id))


def get_list_view_btn(id_):
    return ViewLink(
        "Liste des fournisseurs", "list_suppliers", path="company_suppliers", id=id_
    )


def get_view_btn(supplier_id):
    return ViewLink(
        "Revenir au fournisseur", "view_supplier", path="supplier", id=supplier_id
    )


def get_edit_btn(supplier_id):
    return ViewLink(
        "Modifier",
        "edit_supplier",
        path="supplier",
        id=supplier_id,
        _query=dict(action="edit"),
    )


class SupplierImportStep1(CsvFileUploadView):
    title = "Import des fournisseurs, étape 1 : chargement d'un fichier au \
format csv"
    model_types = ("suppliers",)
    default_model_type = "suppliers"

    def get_next_step_route(self, args):
        return self.request.route_path(
            "company_suppliers_import_step2", id=self.context.id, _query=args
        )


class SupplierImportStep2(ConfigFieldAssociationView):
    title = "Import de fournisseurs, étape 2 : associer les champs"
    model_types = SupplierImportStep1.model_types

    def get_previous_step_route(self):
        return self.request.route_path(
            "company_suppliers_import_step1",
            id=self.context.id,
        )

    def get_default_values(self):
        log.info("Asking for default values : %s" % self.context.id)
        return dict(company_id=self.context.id)


def includeme(config):
    """
    Add module's views
    """
    config.add_view(
        SupplierAdd,
        route_name="company_suppliers",
        renderer="supplier_edit.mako",
        request_method="POST",
        permission="add_supplier",
    )

    config.add_view(
        SupplierAdd,
        route_name="company_suppliers",
        renderer="supplier_edit.mako",
        request_param="action=add",
        permission="add_supplier",
    )

    config.add_view(
        SupplierEdit,
        route_name="supplier",
        renderer="supplier_edit.mako",
        request_param="action=edit",
        permission="edit_supplier",
    )

    config.add_view(
        make_redirect_view("supplier_running_orders", True),
        route_name="supplier",
        request_method="GET",
        permission="view_supplier",
    )
    config.add_view(
        SupplierViewRunningOrders,
        route_name="supplier_running_orders",
        renderer="/supplier/supplier_list_of_orders.mako",
        request_method="GET",
        permission="view_supplier",
        layout="supplier",
    )
    config.add_view(
        SupplierViewInvoicedOrders,
        route_name="supplier_invoiced_orders",
        renderer="/supplier/supplier_list_of_invoiced_orders.mako",
        request_method="GET",
        permission="view_supplier",
        layout="supplier",
    )
    config.add_view(
        SupplierViewInvoices,
        route_name="supplier_invoices",
        renderer="/supplier/supplier_list_of_invoices.mako",
        request_method="GET",
        permission="view_supplier",
        layout="supplier",
    )

    config.add_view(
        SupplierViewExpenseLines,
        route_name="supplier_expenselines",
        renderer="/supplier/supplier_list_of_expenselines.mako",
        request_method="GET",
        permission="view_supplier",
        layout="supplier",
    )

    config.add_view(
        supplier_delete,
        route_name="supplier",
        request_param="action=delete",
        permission="delete_supplier",
        request_method="POST",
        require_csrf=True,
    )
    config.add_view(
        supplier_archive,
        route_name="supplier",
        request_param="action=archive",
        permission="edit_supplier",
        request_method="POST",
        require_csrf=True,
    )

    config.add_view(
        SupplierImportStep1,
        route_name="company_suppliers_import_step1",
        permission="add_supplier",
        renderer="base/formpage.mako",
    )

    config.add_view(
        SupplierImportStep2,
        route_name="company_suppliers_import_step2",
        permission="add_supplier",
        renderer="base/formpage.mako",
    )

    config.add_company_menu(
        parent="supply",
        order=1,
        label="Fournisseurs",
        route_name="company_suppliers",
        route_id_key="company_id",
        routes_prefixes=["supplier"],
    )
