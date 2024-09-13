import datetime
from typing import Dict

from pyramid.httpexceptions import HTTPFound

from caerp.resources import supplier_order_resources
from caerp.views import (
    BaseListView,
    BaseView,
    DeleteView,
    DuplicateView,
    submit_btn,
    JsAppViewMixin,
)
from caerp.views.files.views import (
    FileUploadView,
)
from caerp.forms.supply.supplier_order import get_supplier_orders_list_schema
from caerp.models.supply import (
    SupplierInvoice,
    SupplierOrder,
)
from caerp.models.third_party.supplier import Supplier
from caerp.utils.widgets import (
    ViewLink,
    Link,
    POSTButton,
)
from caerp.views import (
    BaseFormView,
)
from caerp.views.supply.base_views import SupplierDocListTools
from caerp.forms.supply.supplier_order import get_supplier_order_add_schema

from caerp.views.supply.orders.routes import (
    COLLECTION_ROUTE,
    ITEM_ROUTE,
    COMPANY_COLLECTION_ROUTE,
)
from caerp.views.supply.utils import get_supplier_doc_url


def populate_actionmenu(request):
    return request.actionmenu.add(
        ViewLink(
            "Revenir à la liste des commandes fournisseur",
            path=COMPANY_COLLECTION_ROUTE,
            id=request.context.get_company_id(),
        )
    )


def _default_order_name(supplier):
    return "Commande {}, {}".format(
        supplier.label,
        datetime.date.today(),
    )


class SupplierOrderAddView(BaseFormView):
    add_template_vars = ("title",)
    title = "Saisir une commande fournisseur"

    schema = get_supplier_order_add_schema()
    buttons = (submit_btn,)

    def before(self, form):
        assert self.context.__name__ == "company"
        form.set_appstruct({"company_id": self.context.id})

    def submit_success(self, appstruct):
        assert self.context.__name__ == "company"
        appstruct["company_id"] = self.context.id

        supplier = Supplier.get(appstruct["supplier_id"])

        appstruct["name"] = _default_order_name(supplier)

        obj = SupplierOrder(**appstruct)

        self.dbsession.add(obj)
        self.dbsession.flush()
        edit_url = get_supplier_doc_url(
            self.request,
            doc=obj,
        )
        return HTTPFound(edit_url)


class SupplierOrderEditView(BaseView, JsAppViewMixin):
    """
    Can act as edit view or readonly view (eg: waiting for validation).
    """

    def context_url(self, _query: Dict[str, str] = {}):
        return get_supplier_doc_url(self.request, _query=_query, api=True)

    @property
    def title(self):
        label = self.context.name
        if self.context.internal:
            label += " (Commande interne)"
        return label

    def more_js_app_options(self):
        return dict(
            edit=bool(self.request.has_permission("edit.supplier_order")),
        )

    def __call__(self):
        populate_actionmenu(self.request)
        supplier_order_resources.need()
        return dict(
            title=self.title,
            context=self.context,
            js_app_options=self.get_js_app_options(),
        )


class SupplierOrderDuplicateView(DuplicateView):
    route_name = ITEM_ROUTE
    message = "vous avez été redirigé vers la nouvelle commande fournisseur"

    def on_duplicate(self, item):
        src_order = self.context
        target_order = item

        target_order.name = "Copie de {}".format(src_order.name)
        target_order.import_lines_from_order(src_order)
        self.dbsession.merge(target_order)
        self.dbsession.flush()


class CompanySupplierOrderListTools(SupplierDocListTools):
    model_class = SupplierOrder

    sort_columns = {
        "cae_percentage": "cae_percentage",
        "supplier_invoice": "supplier_invoice_id",
    }
    sort_columns.update(SupplierDocListTools.sort_columns)

    def filter_invoice_status(self, query, appstruct):
        invoice_status = appstruct["invoice_status"]
        if invoice_status in ("present", "draft", "valid", "resulted"):
            query = query.filter(SupplierOrder.supplier_invoice_id != None)  # noqa
            query = query.join(SupplierOrder.supplier_invoice)
            if invoice_status == "draft":
                query = query.filter(SupplierInvoice.status == "draft")
            elif invoice_status == "valid":
                query = query.filter(SupplierInvoice.status == "valid")
            elif invoice_status == "resulted":
                query = query.filter(SupplierInvoice.paid_status == "resulted")
        elif invoice_status == "absent":
            query = query.filter(SupplierOrder.supplier_invoice_id == None)  # noqa
        return query


def stream_supplier_order_actions(request, supplier_order):
    yield Link(
        get_supplier_doc_url(request, doc=supplier_order),
        "Voir ou modifier",
        icon="arrow-right",
    )
    delete_allowed = request.has_permission(
        "delete.supplier_order",
        supplier_order,
    )
    if delete_allowed:
        yield POSTButton(
            get_supplier_doc_url(
                request,
                doc=supplier_order,
                _query=dict(action="delete"),
            ),
            "Supprimer",
            title="Supprimer définitivement cette commande ?",
            icon="trash-alt",
            css="negative",
            confirm="Êtes-vous sûr de vouloir supprimer cette commande ?",
        )


class BaseSupplierOrderListView(
    CompanySupplierOrderListTools,
    BaseListView,
):
    title = "Liste des commandes fournisseurs"
    add_template_vars = ["title", "stream_actions"]

    def stream_actions(self, supplier_order):
        return stream_supplier_order_actions(self.request, supplier_order)


class AdminSupplierOrderListView(BaseSupplierOrderListView):
    """
    Admin-level view, listing all orders from all companies.
    """

    is_admin_view = True
    add_template_vars = BaseSupplierOrderListView.add_template_vars + [
        "is_admin_view",
    ]

    schema = get_supplier_orders_list_schema(is_global=True)

    def query(self):
        return SupplierOrder.query()


class CompanySupplierOrderListView(BaseSupplierOrderListView):
    """
    Company-scoped SupplierOrder list view.
    """

    schema = get_supplier_orders_list_schema(is_global=False)

    def query(self):
        company = self.request.context
        return SupplierOrder.query().filter_by(company_id=company.id)


class SupplierOrderDeleteView(DeleteView):
    delete_msg = "La commande fournisseur a bien été supprimée"

    def redirect(self):
        return HTTPFound(
            self.request.route_path(
                COMPANY_COLLECTION_ROUTE, id=self.context.company.id
            )
        )


def includeme(config):
    # Admin views
    config.add_view(
        AdminSupplierOrderListView,
        request_method="GET",
        route_name=COLLECTION_ROUTE,
        permission="admin.supplier_order",
        renderer="/supply/supplier_orders.mako",
    )

    # Company views
    config.add_view(
        SupplierOrderAddView,
        route_name=COMPANY_COLLECTION_ROUTE,
        request_param="action=new",
        permission="add.supplier_order",
        renderer="base/formpage.mako",
    )

    config.add_view(
        CompanySupplierOrderListView,
        route_name=COMPANY_COLLECTION_ROUTE,
        request_method="GET",
        renderer="/supply/supplier_orders.mako",
        permission="list.supplier_order",
    )
    config.add_view(
        SupplierOrderEditView,
        route_name=ITEM_ROUTE,
        renderer="/supply/supplier_order.mako",
        permission="view.supplier_order",
        layout="opa",
    )

    config.add_view(
        SupplierOrderDeleteView,
        route_name=ITEM_ROUTE,
        request_param="action=delete",
        permission="delete.supplier_order",
        request_method="POST",
        require_csrf=True,
    )

    config.add_view(
        SupplierOrderDuplicateView,
        route_name=ITEM_ROUTE,
        request_param="action=duplicate",
        permission="duplicate.supplier_order",
        request_method="POST",
        require_csrf=True,
    )

    # File attachment
    config.add_view(
        FileUploadView,
        route_name=f"{ITEM_ROUTE}/addfile",
        renderer="base/formpage.mako",
        permission="add.file",
    )

    config.add_admin_menu(
        parent="sale",
        order=3,
        label="Commandes fournisseurs",
        href=COLLECTION_ROUTE,
        routes_prefixes=[ITEM_ROUTE],
    )
    config.add_company_menu(
        parent="supply",
        order=1,
        label="Commandes fournisseurs",
        route_name=COMPANY_COLLECTION_ROUTE,
        route_id_key="company_id",
        routes_prefixes=[ITEM_ROUTE],
    )
