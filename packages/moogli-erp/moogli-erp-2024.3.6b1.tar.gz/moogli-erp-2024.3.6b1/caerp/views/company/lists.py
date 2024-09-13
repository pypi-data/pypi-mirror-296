import colander

from caerp.models.company import Company
from caerp.forms.company import get_list_schema
from caerp.utils.widgets import Link, POSTButton
from caerp.views import BaseListView, BaseView

from .tools import get_company_url
from .routes import COLLECTION_MAP_ROUTE, COLLECTION_ROUTE


class CompanySearchTools:
    def filter_include_inactive(self, query, appstruct):
        include_inactive = appstruct.get("include_inactive", False)

        if include_inactive in ("false", False, colander.null):
            query = query.filter_by(active=True)

        return query

    def filter_include_internal(self, query, appstruct):
        include_internal = appstruct.get("include_internal", False)

        if include_internal in ("false", False, colander.null):
            query = query.filter_by(internal=False)

        return query

    def filter_search(self, query, appstruct):
        search = appstruct.get("search")
        if search:
            query = query.filter(Company.name.like("%" + search + "%"))
        return query


class CompanyList(CompanySearchTools, BaseListView):
    title = "Annuaire des enseignes"
    schema = get_list_schema()
    sort_columns = dict(name=Company.name)
    default_sort = "name"
    default_direction = "asc"

    add_template_vars = (
        "title",
        "stream_actions",
    )

    def query(self):
        return Company.query(active=False)

    def _get_item_url(self, company, action=None):
        query = {}
        if action:
            query["action"] = "disable"
        return get_company_url(self.request, company, action=action)

    def stream_actions(self, company):
        yield Link(
            self._get_item_url(company),
            "Modifier",
            title="Modifier l'enseigne",
            icon="pen",
            css="icon",
        )
        url = self._get_item_url(company, action="disable")
        if company.active:
            yield POSTButton(
                url,
                "Désactiver",
                title="Désactiver l'enseigne",
                icon="lock",
                css="icon",
            )
        else:
            yield POSTButton(
                url,
                "Activer",
                title="Activer l'enseigne",
                icon="lock-open",
                css="icon",
            )


class CompanyListMap(BaseView):
    title = "Annuaire des enseignes"

    def __call__(self) -> dict:
        from caerp.resources import company_map_js

        company_map_js.need()

        if self.request.has_permission("admin_companies"):
            tab_title = "Liste des Enseignes"
            tab_url = "/companies"
        else:
            tab_title = "Liste des Utilisateurs"
            tab_url = "/users"

        result = {
            "title": self.title,
            "js_app_options": {
                "tab_title": tab_title,
                "tab_url": tab_url,
            },
        }
        return result


def includeme(config):
    config.add_view(
        CompanyList,
        route_name=COLLECTION_ROUTE,
        renderer="companies.mako",
        permission="admin_companies",
    )

    config.add_view(
        CompanyListMap,
        route_name=COLLECTION_MAP_ROUTE,
        permission="view",
        renderer="base/vue_app.mako",
        layout="vue_opa",
    )
