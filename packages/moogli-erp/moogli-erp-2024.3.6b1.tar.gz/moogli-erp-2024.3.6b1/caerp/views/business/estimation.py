from pyramid.httpexceptions import HTTPFound
from caerp.models.task import Estimation
from caerp.forms.tasks.estimation import get_list_schema
from caerp.views.estimations.lists import CompanyEstimationList
from caerp.views import TreeMixin
from caerp.views.business.routes import (
    BUSINESS_ITEM_ESTIMATION_ROUTE,
)
from caerp.views.project.business import ProjectBusinessListView


class BusinessEstimationList(CompanyEstimationList, TreeMixin):
    route_name = BUSINESS_ITEM_ESTIMATION_ROUTE
    schema = get_list_schema(
        is_global=False,
        excludes=(
            "company_id",
            "year",
            "customer",
        ),
    )
    add_template_vars = (
        "title",
        "is_admin",
        "with_draft",
        "add_url",
    )

    @property
    def add_url(self):
        return self.request.route_path(
            self.route_name, id=self.request.context.id, _query={"action": "add"}
        )

    @property
    def title(self):
        return "Devis du dossier {0}".format(self.request.context.name)

    def _get_company_id(self, appstruct=None):
        """
        Return the current context's company id
        """
        return self.request.context.project.company_id

    def filter_business(self, query, appstruct):
        self.populate_navigation()
        query = query.filter(Estimation.business_id == self.context.id)
        return query


def add_estimation_view(context, request):
    """
    View used to add an estimation to the current business
    """
    estimation = context.add_estimation(request, request.identity)
    return HTTPFound(request.route_path("/estimations/{id}", id=estimation.id))


def includeme(config):
    config.add_tree_view(
        BusinessEstimationList,
        parent=ProjectBusinessListView,
        renderer="project/estimations.mako",
        permission="list.estimations",
        layout="business",
    )
    config.add_view(
        add_estimation_view,
        route_name=BUSINESS_ITEM_ESTIMATION_ROUTE,
        permission="add.estimation",
        request_param="action=add",
        layout="default",
        request_method="POST",
        require_csrf=True,
    )
