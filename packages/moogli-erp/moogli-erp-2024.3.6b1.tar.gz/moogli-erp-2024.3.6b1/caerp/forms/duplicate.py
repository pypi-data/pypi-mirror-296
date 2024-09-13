import colander
from deform import widget
from caerp.models.project import Project, Phase
from caerp.models.third_party.customer import Customer
from caerp import forms
from caerp.forms.third_party.customer import (
    get_company_customers_from_request,
    customer_choice_node_factory,
)


def get_current_customer_id_from_request(request):
    """
    Return the current customer from the given request

    context is a Task here, so it has a customer_id
    """
    return request.context.customer_id


@colander.deferred
def deferred_default_customer(node, kw):
    request = kw["request"]
    return get_current_customer_id_from_request(request)


def get_project_options(request):
    customer_id = get_current_customer_id_from_request(request)
    projects = Project.label_query().filter_by(customer_id=customer_id)
    return [(pro.id, "%s (%s)" % (pro.name, pro.code)) for pro in projects]


@colander.deferred
def deferred_project_choice(node, kw):
    projects = get_project_options(kw["request"])
    return widget.SelectWidget(values=projects)


def get_current_project_from_request(request):
    return request.context.project


@colander.deferred
def deferred_default_project(node, kw):
    request = kw["request"]
    return get_current_project_from_request(request).id


def get_phases_options(request):
    project = get_current_project_from_request(request)
    return [(phase.id, phase.name) for phase in project.phases]


@colander.deferred
def deferred_phase_choice(node, kw):
    phases = get_phases_options(kw["request"])
    return widget.SelectWidget(values=phases)


@colander.deferred
def deferred_default_phase(node, kw):
    request = kw["request"]
    return request.context.phase.id


def get_all_projects(request):
    query = Project.label_query()
    customer_ids = [c.id for c in get_company_customers_from_request(request)]

    projects = query.filter(Project.customers.any(Customer.id.in_(customer_ids)))
    return projects.all()


@colander.deferred
def deferred_project_validator(node, kw):
    projects = get_all_projects(kw["request"])
    return colander.OneOf([p.id for p in projects])


def get_all_phases(request):
    project_ids = [p.id for p in get_all_projects(request)]
    return Phase.query().filter(Phase.project_id.in_(project_ids)).all()


@colander.deferred
def deferred_phase_validator(node, kw):
    phases = get_all_phases(kw["request"])
    return colander.OneOf([p.id for p in phases])


class DuplicateSchema(colander.MappingSchema):
    """
    colander schema for duplication recording
    """

    customer = customer_choice_node_factory()
    project = colander.SchemaNode(
        colander.Integer(),
        title="Dossier",
        widget=deferred_project_choice,
        default=deferred_default_project,
        validator=deferred_project_validator,
    )
    phase = colander.SchemaNode(
        colander.Integer(),
        title="Phase",
        widget=deferred_phase_choice,
        default=deferred_default_phase,
        validator=deferred_phase_validator,
    )


class EditMetadataSchema(colander.MappingSchema):
    """
    Colander schema for moving a task from a phase to another
    """

    name = colander.SchemaNode(
        colander.String(),
        title="Nom du document",
        validator=colander.Length(max=255),
        missing="",
    )
    date = forms.today_node(title="Date")
    phase_id = colander.SchemaNode(
        colander.Integer(),
        title="Phase",
        widget=deferred_phase_choice,
        validator=deferred_phase_validator,
    )


def remove_some_fields(schema, kw):
    request = kw["request"]

    if len(request.context.project.phases) == 1:
        del schema["phase_id"]

    if not request.has_permission("admin_task"):
        del schema["date"]

    return schema


EDIT_METADATASCHEMA = EditMetadataSchema(after_bind=remove_some_fields)
