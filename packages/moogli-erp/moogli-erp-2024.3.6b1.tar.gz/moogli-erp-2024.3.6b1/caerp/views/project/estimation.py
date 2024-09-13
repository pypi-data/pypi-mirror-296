from caerp.models.task import Estimation
from caerp.forms.tasks.estimation import get_list_schema
from caerp.views.estimations.lists import CompanyEstimationList
from caerp.views import TreeMixin
from caerp.views.company.routes import COMPANY_ESTIMATION_ADD_ROUTE
from caerp.views.project.routes import PROJECT_ITEM_ESTIMATION_ROUTE
from caerp.views.project.project import (
    ProjectListView,
)


class ProjectEstimationListView(CompanyEstimationList, TreeMixin):
    route_name = PROJECT_ITEM_ESTIMATION_ROUTE
    schema = get_list_schema(
        is_global=False,
        excludes=(
            "company_id",
            "year",
            "customer",
        ),
    )
    add_template_vars = CompanyEstimationList.add_template_vars + ("add_url",)

    @property
    def add_url(self):
        return self.request.route_path(
            COMPANY_ESTIMATION_ADD_ROUTE,
            id=self.context.company_id,
            _query={"project_id": self.context.id},
        )

    @property
    def title(self):
        return "Devis du dossier {0}".format(self.request.context.name)

    def _get_company_id(self, appstruct=None):
        """
        Return the current context's company id
        """
        return self.request.context.company_id

    def filter_project(self, query, appstruct):
        self.populate_navigation()
        query = query.filter(Estimation.project_id == self.context.id)
        return query


def includeme(config):
    config.add_tree_view(
        ProjectEstimationListView,
        parent=ProjectListView,
        renderer="project/estimations.mako",
        permission="list_estimations",
        layout="project",
    )
