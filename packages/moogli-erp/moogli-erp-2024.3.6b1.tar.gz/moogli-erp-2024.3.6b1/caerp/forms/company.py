"""
    Company form schemas
"""
from caerp.utils.compat import Iterable
import logging
from typing import Union

import colander
import colanderalchemy
import deform
import deform_extensions
from functools import partial
from sqlalchemy.orm.query import Query

from caerp.models.company import (
    CompanyActivity,
    Company,
)
from caerp.models.user.login import Login
from caerp.models.user.user import User
from caerp.models.project.types import ProjectType
from caerp import forms
from caerp.forms.custom_types import QuantityType
from caerp.forms import (
    files,
    lists,
)
from caerp.utils.image import (
    ImageResizer,
    ImageRatio,
)
from caerp.forms.user import (
    get_antenne_options,
    get_deferred_user_choice,
)

DECIMAL_TO_DISPLAY_VALUES = (
    ("2", "2 décimales (1,25 €)"),
    ("5", "5 décimales (1,24952€)"),
)

log = logging.getLogger(__name__)

HEADER_RATIO = ImageRatio(4, 1)
HEADER_RESIZER = ImageResizer(2000, 500)
LOGO_RESIZER = ImageResizer(800, 800)


@colander.deferred
def deferred_edit_adminonly_widget(node, kw):
    """
    return a deferred adminonly edit widget
    """
    request = kw["request"]
    if not request.has_permission("admin_company", request.context):
        return deform_extensions.DisabledInput()
    else:
        return deform.widget.TextInputWidget()


@colander.deferred
def deferred_company_datas_select(node, kw):
    values = CompanyActivity.query("id", "label").all()
    values.insert(0, ("", "- Sélectionner un type d'activité"))
    return deform.widget.SelectWidget(values=values)


@colander.deferred
def deferred_company_antenne_select(node, kw):
    antenne_options = get_antenne_options()
    antenne_options.insert(0, ("", "- Sélectionner une antenne"))
    return deform.widget.SelectWidget(values=antenne_options)


@colander.deferred
def deferred_company_datas_validator(node, kw):
    ids = [entry[0] for entry in CompanyActivity.query("id")]
    return colander.OneOf(ids)


def customize_company_schema(schema):
    customize = partial(forms.customize_field, schema)
    schema["user_id"] = forms.id_node()
    schema["come_from"] = forms.come_from_node()
    customize(
        "name",
        widget=deferred_edit_adminonly_widget,
        section="Informations publiques",
    )
    customize("email", validator=forms.mail_validator())

    for attr in ("contribution", "insurance"):
        for prefix in ("", "internal"):
            field = "{}{}".format(prefix, attr)
            if field in schema:
                customize(
                    field,
                    typ=QuantityType(),
                    widget=deform.widget.TextInputWidget(input_append="%"),
                    validator=colander.Range(
                        min=0,
                        max=100,
                        min_err="Veuillez fournir un nombre supérieur à 0",
                        max_err="Veuillez fournir un nombre inférieur à 100",
                    ),
                    missing=None,
                )
    customize(
        "cgv",
        widget=forms.richtext_widget(),
    )
    customize(
        "decimal_to_display",
        widget=deform.widget.SelectWidget(
            values=DECIMAL_TO_DISPLAY_VALUES,
        ),
    )

    if "activities" in schema:
        child_node = forms.get_sequence_child_item(CompanyActivity)
        child_node[0].title = "un domaine"
        customize(
            "activities",
            children=child_node,
            description="""<b>Activité principale :</b> Le premier domaine d'activité
            de la liste sera considéré comme l'activité principale de l'enseigne pour
            l'analyse commerciale""",
        )

    customize(
        "antenne_id",
        widget=deferred_company_antenne_select,
    )

    customize(
        "follower_id",
        get_deferred_user_choice(
            roles=["admin", "manager"],
            widget_options={
                "default_option": ("", "- Sélectionner un accompagnateur"),
            },
        ),
    )

    customize("margin_rate", typ=QuantityType(), validator=colander.Range(0, 0.9999))
    customize(
        "general_overhead", typ=QuantityType(), validator=colander.Range(0, 9.9999)
    )

    customize(
        "address",
        description="Astuce : ce champ initialise la position sur la carte des enseignes.",
    )
    customize(
        "zip_code",
        description="Astuce : ce champ initialise la position sur la carte des enseignes.",
    )
    return schema


def get_company_schema(admin=False, excludes=()) -> colander.SchemaNode:
    """
    Build company add/edit form schema
    """
    default_excludes = (
        "id",
        "created_at",
        "updated_at",
        "active",
        "bank_account",
        "comments",
    )
    if (
        ProjectType.query()
        .filter(ProjectType.include_price_study == 1, ProjectType.active == 1)
        .count()
        == 0
    ):
        default_excludes += (
            "general_overhead",
            "margin_rate",
            "use_margin_rate_in_catalog",
        )
    if not admin:
        default_excludes += (
            "antenne_id",
            "follower_id",
            "RIB",
            "IBAN",
            "contribution",
            "internalcontribution",
            "insurance",
            "internalinsurance",
            "internal",
            "code_compta",
            "general_customer_account",
            "third_party_customer_account",
            "general_supplier_account",
            "third_party_supplier_account",
            "internalgeneral_customer_account",
            "internalthird_party_customer_account",
            "internalgeneral_supplier_account",
            "internalthird_party_supplier_account",
            "general_expense_account",
        )
    excludes = tuple(excludes) + default_excludes
    schema = colanderalchemy.SQLAlchemySchemaNode(Company, excludes=excludes)
    schema = customize_company_schema(schema)
    return schema


def get_deferred_company_choices(widget_options):
    """
    Build a deferred for company selection widget

    Available widget_options :

        default_option

            A default option that will be inserted in the list

        active_only

            Should we restrict the query to active companies ?

        query

            default None: All companies are returned

            Can be a callable or a list of fixed elements
            The callable should return a list of 2-uples (id, label)
            The function should take a kw parameter.
            kw are the colander schema binding parameters
    """
    default_option = widget_options.pop("default_option", None)
    active_only = widget_options.get("active_only", False)
    more_options = widget_options.get("more_options")
    query = widget_options.get("query")

    @colander.deferred
    def deferred_company_choices(node, kw):
        """
        return a deferred company selection widget
        """
        if query is None:
            values = Company.get_companies_select_datas(kw["request"], active_only)
        elif callable(query):
            values = query(kw["request"]).all()
        elif isinstance(query, Query):
            raise Exception(
                "No query accepted here, a callable returning a query "
                "should be provided"
            )
        else:
            values = query

        if more_options:
            for option in more_options:
                values.insert(0, option)
        if default_option:
            # Clean fix would be to replace that default_option 2-uple arg with
            # a placeholder str arg, as in JS code.
            widget_options["placeholder"] = default_option[1]
            values.insert(0, default_option)

        return deform.widget.Select2Widget(values=values, **widget_options)

    return deferred_company_choices


def company_node(multiple=False, **kw):
    """
    Return a schema node for company selection
    """
    widget_options = kw.pop("widget_options", {})
    return colander.SchemaNode(
        colander.Set() if multiple else colander.Integer(),
        widget=get_deferred_company_choices(widget_options),
        **kw,
    )


company_choice_node = forms.mk_choice_node_factory(
    company_node,
    resource_name="une enseigne",
    resource_name_plural="de zéro à plusieurs enseignes",
)

company_filter_node_factory = forms.mk_filter_node_factory(
    company_node,
    title="Enseigne",
    empty_filter_msg="Toutes",
)


def get_list_schema():
    """
    Return a schema for filtering companies list
    """
    schema = lists.BaseListsSchema().clone()
    schema["search"].title = "Nom de l'enseigne"
    schema.add(
        colander.SchemaNode(
            colander.Boolean(),
            name="include_inactive",
            title="",
            label="Inclure les enseignes désactivées",
            default=False,
            missing=False,
        )
    )
    schema.add(
        colander.SchemaNode(
            colander.Boolean(),
            name="include_internal",
            title="",
            label="Inclure les enseignes internes à la CAE",
            default=False,
            missing=False,
        )
    )
    return schema


def get_mapsearch_schema():
    """
    return a schema for filtering companies on map
    """
    schema = lists.BaseListsSchema().clone()
    schema["search"].title = "Nom, enseigne, activité"
    schema.add(
        colander.SchemaNode(
            colander.Integer(),
            name="activity_id",
            title="Type d'activité",
            missing=colander.drop,
            widget=deferred_company_datas_select,
            validator=deferred_company_datas_validator,
        )
    )
    schema.add(
        colander.SchemaNode(
            colander.String(),
            name="postcode",
            missing=colander.drop,
        )
    )

    return schema


def get_deferred_company_attr_default(attrname):
    """
    Build a deferred default value returning the value of the company attribute
    attrname

    NB : Expects the request.context to be a company or to have a
    request.context.company

    :param str attrname: Name of the company attribute to retrieve
    :rtype: colander.deferred
    """

    @colander.deferred
    def deferred_value(node, kw):
        context = kw["request"].context
        if isinstance(context, Company):
            value = getattr(context, attrname)
        elif hasattr(context, "company"):
            value = getattr(context.company, attrname)
        else:
            value = 0
        return value

    return deferred_value


def get_employees_from_request(request) -> Iterable[User]:
    assert isinstance(request.context, Company)
    query = User.query().join(Company.employees).join(User.login)
    query = query.filter(
        Company.id == request.context.id,
        Login.active == True,  # noqa E712
    )
    return query


def get_default_employee_from_request(request) -> Union[User, None]:
    """
    Preselects the employee if there is only one or if it is the currently
    logged user, else no default : up for selection.
    """
    query = get_employees_from_request(request)
    if query.count() > 1:
        # If I am a company user, select me by default
        # May return None else, which is expected
        logged_company_user = query.filter(User.id == request.identity.id).first()
        if logged_company_user is None:
            return None
        else:
            return logged_company_user
    else:
        return query.first()
