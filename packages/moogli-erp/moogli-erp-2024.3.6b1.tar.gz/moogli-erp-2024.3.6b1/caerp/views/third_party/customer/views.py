import deform
import logging
import re
import typing

from pyramid.httpexceptions import HTTPFound

from caerp.forms.third_party.customer import CustomerAddToProjectSchema
from caerp.models.project.project import Project
from caerp.resources import node_view_only_js
from caerp.utils.accounting import is_customer_accounting_by_tva
from caerp.utils.widgets import (
    Link,
    POSTButton,
)
from caerp.views import (
    BaseFormView,
    BaseView,
    TreeMixin,
    submit_btn,
    JsAppViewMixin,
)
from caerp.views.csv_import import (
    CsvFileUploadView,
    ConfigFieldAssociationView,
)
from caerp.views.project.routes import (
    COMPANY_PROJECTS_ROUTE,
)
from caerp.views.third_party.customer.lists import CustomersListView

from .base import get_customer_url
from .controller import CustomerAddEditController
from .routes import (
    COMPANY_CUSTOMERS_ROUTE,
    COMPANY_CUSTOMERS_ADD_ROUTE,
    API_COMPANY_CUSTOMERS_ROUTE,
    CUSTOMER_ITEM_ROUTE,
)


logger = logging.getLogger(__name__)


class CustomerView(BaseFormView, JsAppViewMixin, TreeMixin):
    """
    Return the view of a customer
    """

    route_name = CUSTOMER_ITEM_ROUTE

    @property
    def tree_url(self):
        return self.request.route_path(self.route_name, id=self.context.id)

    @property
    def title(self):
        return f"Client : {self.context.label}"

    def get_company_projects_form(self):
        """
        Return a form object for project add
        :param obj request: The pyramid request object
        :returns: A form
        :rtype: class:`deform.Form`
        """
        schema = CustomerAddToProjectSchema().bind(
            request=self.request, context=self.context
        )
        form = deform.Form(
            schema,
            buttons=(submit_btn,),
            action=self.request.route_path(
                "customer", id=self.context.id, _query={"action": "addcustomer"}
            ),
        )
        return form

    def context_url(self, _query: typing.Dict[str, str] = {}):
        return self.request.route_url(
            "/api/v1/customers/{id}", id=self.context.id, _query=_query
        )

    def stream_project_actions(self, project: Project):
        from caerp.views.project.routes import PROJECT_ITEM_ROUTE
        from caerp.views.company.routes import (
            COMPANY_ESTIMATION_ADD_ROUTE,
            COMPANY_INVOICE_ADD_ROUTE,
        )

        yield Link(
            self.request.route_path(PROJECT_ITEM_ROUTE, id=project.id),
            label="Voir ce dossier",
            title="Voir ou modifier ce dossier",
            icon="arrow-right",
            css="btn-icon",
        )
        if not project.archived:
            yield Link(
                self.request.route_path(
                    COMPANY_ESTIMATION_ADD_ROUTE,
                    id=self.context.company_id,
                    _query={"project_id": project.id, "customer_id": self.context.id},
                ),
                label="Ajouter un devis",
                icon="file-list",
                css="btn-icon",
            )
            if self.request.has_permission("add.invoice", project):
                yield Link(
                    self.request.route_path(
                        COMPANY_INVOICE_ADD_ROUTE,
                        id=self.context.company_id,
                        _query={
                            "project_id": project.id,
                            "customer_id": self.context.id,
                        },
                    ),
                    label="Ajouter une facture",
                    icon="file-invoice-euro",
                    css="btn-icon",
                )
            yield POSTButton(
                self.request.route_path(
                    PROJECT_ITEM_ROUTE, id=project.id, _query={"action": "archive"}
                ),
                label="Archiver ce dossier",
                confirm="Êtes-vous sûr de vouloir archiver ce dossier ?",
                icon="archive",
                css="btn-icon",
            )
        elif self.request.has_permission("delete_project", project):
            yield POSTButton(
                self.request.route_path(
                    PROJECT_ITEM_ROUTE, id=project.id, _query={"action": "delete"}
                ),
                label="Supprimer ce dossier",
                confirm="Êtes-vous sûr de vouloir supprimer définitivement ce dossier ?",
                icon="trash-alt",
                css="btn-icon negative",
            )

    def __call__(self):
        self.populate_navigation()
        node_view_only_js.need()

        title = "Client : {0}".format(self.context.label)
        if self.request.context.code:
            title += " {0}".format(self.context.code)

        return dict(
            title=title,
            customer=self.request.context,
            project_form=self.get_company_projects_form(),
            add_project_url=self.request.route_path(
                COMPANY_PROJECTS_ROUTE,
                id=self.context.company.id,
                _query={"action": "add", "customer": self.context.id},
            ),
            js_app_options=self.get_js_app_options(),
            stream_project_actions=self.stream_project_actions,
            display_accounting_config=not is_customer_accounting_by_tva(self.request),
        )


def customer_archive(request):
    """
    Archive the current customer
    """
    customer = request.context
    if not customer.archived:
        customer.archived = True
    else:
        customer.archived = False
    request.dbsession.merge(customer)
    return HTTPFound(request.referer)


def customer_delete(request):
    """
    Delete the current customer
    """
    customer = request.context
    company_id = customer.company_id
    request.dbsession.delete(customer)
    request.session.flash("Le client '{0}' a bien été supprimé".format(customer.label))
    # On s'assure qu'on ne redirige pas vers la route courante
    if re.compile(".*customers/[0-9]+.*").match(request.referer):
        redirect = request.route_path(COMPANY_CUSTOMERS_ROUTE, id=company_id)
    else:
        redirect = request.referer
    return HTTPFound(redirect)


class CustomerAddToProject(BaseFormView):
    """
    Catch customer id and update project customers
    """

    schema = CustomerAddToProjectSchema()
    validation_msg = "Le dossier a été ajouté avec succès"

    def submit_success(self, appstruct):
        project_id = appstruct["project_id"]
        project = self.dbsession.query(Project).filter_by(id=project_id).one()
        if self.context not in project.customers:
            project.customers.append(self.context)
            self.dbsession.flush()
        self.session.flash(self.validation_msg)
        redirect = get_customer_url(self.request)
        return HTTPFound(redirect)


class CustomerAddView(BaseView, JsAppViewMixin, TreeMixin):
    title = "Ajouter un client"
    controller_class = CustomerAddEditController
    edit = False
    route_name = COMPANY_CUSTOMERS_ADD_ROUTE

    def __init__(self, context, request=None):
        super().__init__(context, request)
        self.controller = self.controller_class(self.request, edit=self.edit)

    def context_url(self, _query={}):
        return self.request.route_path(
            API_COMPANY_CUSTOMERS_ROUTE, id=self.context.id, _query=_query
        )

    def __call__(self) -> dict:
        from caerp.resources import customer_js

        customer_js.need()
        self.populate_navigation()

        result = {
            "title": self.title,
            "js_app_options": self.get_js_app_options(),
        }
        return result


class CustomerEditView(CustomerAddView, TreeMixin):
    controller_class = CustomerAddEditController
    edit = True
    route_name = CUSTOMER_ITEM_ROUTE

    @property
    def title(self):
        return "Modifier le client '{0}' de l'enseigne '{1}'".format(
            self.context.name, self.context.company.name
        )

    def context_url(self, _query={}):
        return get_customer_url(self.request, api=True, _query=_query)

    def more_js_app_options(self):
        return {
            "customer_id": self.context.id,
            "come_from": self.request.params.get("come_from", None),
        }


class CustomerImportStep1(CsvFileUploadView):
    title = "Import des clients, étape 1 : chargement d'un fichier au \
format csv"
    model_types = ("customers",)
    default_model_type = "customers"

    def get_next_step_route(self, args):
        return self.request.route_path(
            "company_customers_import_step2", id=self.context.id, _query=args
        )


class CustomerImportStep2(ConfigFieldAssociationView):
    title = "Import de clients, étape 2 : associer les champs"
    model_types = CustomerImportStep1.model_types

    def get_previous_step_route(self):
        return self.request.route_path(
            "company_customers_import_step1",
            id=self.context.id,
        )

    def get_default_values(self):
        logger.info("Asking for default values : %s" % self.context.id)
        return dict(company_id=self.context.id)


def includeme(config):
    """
    Add module's views
    """
    for i in range(2):
        index = i + 1
        route_name = "company_customers_import_step%d" % index
        path = r"/company/{id:\d+}/customers/import/%d" % index
        config.add_route(route_name, path, traverse="/companies/{id}")

    config.add_tree_view(
        CustomerView,
        parent=CustomersListView,
        renderer="customers/view.mako",
        request_method="GET",
        permission="view_customer",
        layout="customer",
    )

    config.add_tree_view(
        CustomerAddView,
        parent=CustomersListView,
        renderer="base/vue_app.mako",
        permission="add_customer",
        layout="vue_opa",
    )
    config.add_tree_view(
        CustomerEditView,
        parent=CustomerView,
        renderer="base/vue_app.mako",
        request_param="action=edit",
        permission="edit_customer",
        layout="vue_opa",
    )

    config.add_view(
        customer_delete,
        route_name="customer",
        request_param="action=delete",
        permission="delete_customer",
        request_method="POST",
        require_csrf=True,
    )
    config.add_view(
        customer_archive,
        route_name="customer",
        request_param="action=archive",
        permission="edit_customer",
        request_method="POST",
        require_csrf=True,
    )

    config.add_view(
        CustomerImportStep1,
        route_name="company_customers_import_step1",
        permission="add_customer",
        renderer="base/formpage.mako",
    )

    config.add_view(
        CustomerImportStep2,
        route_name="company_customers_import_step2",
        permission="add_customer",
        renderer="base/formpage.mako",
    )
    config.add_view(
        CustomerAddToProject,
        route_name="customer",
        request_param="action=addcustomer",
        permission="edit_customer",
        renderer="base/formpage.mako",
    )

    config.add_company_menu(
        parent="sale",
        order=0,
        label="Clients",
        route_name=COMPANY_CUSTOMERS_ROUTE,
        route_id_key="company_id",
        routes_prefixes=["customer"],
    )
