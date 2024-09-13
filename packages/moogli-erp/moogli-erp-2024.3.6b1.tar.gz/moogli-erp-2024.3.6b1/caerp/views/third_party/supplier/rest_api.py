from caerp.forms.third_party.supplier import (
    get_edit_internal_supplier_schema,
    get_supplier_schema,
    get_add_edit_supplier_schema,
)
from caerp.models.third_party import Supplier
from caerp.views import BaseRestView
from caerp.views.status.rest_api import StatusLogEntryRestView
from caerp.views.status.utils import get_visibility_options


class SupplierRestView(BaseRestView):
    """
    Supplier rest view

    collection : context Root

        GET : return list of suppliers (company_id should be provided)
    """

    def get_schema(self, submitted):
        if isinstance(self.context, Supplier):
            if self.context.is_internal():
                schema = get_edit_internal_supplier_schema()
            else:
                # Aucune idée comment on arrive ici mais on conserve ce
                # fonctionnement
                if "formid" in submitted:
                    schema = get_supplier_schema()
        else:
            if "formid" in submitted:
                schema = get_supplier_schema()
            else:
                excludes = ("company_id",)
                schema = get_add_edit_supplier_schema(excludes=excludes)
        return schema

    def collection_get(self):
        return self.context.suppliers

    def post_format(self, entry, edit, attributes):
        """
        Associate a newly created element to the parent company
        """
        if not edit:
            entry.company = self.context
        return entry

    def form_config(self):
        return {"options": {"visibilities": get_visibility_options(self.request)}}


def includeme(config):
    config.add_rest_service(
        SupplierRestView,
        "/api/v1/suppliers/{id}",
        collection_route_name="/api/v1/companies/{id}/suppliers",
        view_rights="view_supplier",
        edit_rights="edit_supplier",
        add_rights="add_supplier",
        delete_rights="delete_supplier",
        collection_view_rights="list_suppliers",
    )
    config.add_view(
        SupplierRestView,
        attr="form_config",
        route_name="/api/v1/suppliers/{id}",
        renderer="json",
        request_param="form_config",
        permission="edit_supplier",
    )
    config.add_rest_service(
        StatusLogEntryRestView,
        "/api/v1/suppliers/{eid}/statuslogentries/{id}",
        collection_route_name="/api/v1/suppliers/{id}/statuslogentries",
        collection_view_rights="view_supplier",
        add_rights="view_supplier",
        view_rights="view.statuslogentry",
        edit_rights="edit.statuslogentry",
        delete_rights="delete.statuslogentry",
    )
