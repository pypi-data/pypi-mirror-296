import colander
import deform

from caerp import forms
from caerp.forms.company import company_filter_node_factory
from caerp.forms.third_party.supplier import supplier_filter_node_factory
from caerp.forms.user import follower_filter_node_factory


TYPE_OPTIONS = (
    (
        "both",
        "Tous",
    ),
    (
        "supplier_invoice",
        "Exclure les factures internes",
    ),
    (
        "internalsupplier_invoice",
        "Seulement les factures internes",
    ),
)


def get_list_schema():
    """
    Return a schema for invoice validation listing
    """
    schema = forms.lists.BaseListsSchema().clone()
    del schema["search"]
    schema.insert(
        0,
        colander.SchemaNode(
            colander.String(),
            name="doctype",
            title="Types de factures",
            widget=deform.widget.SelectWidget(values=TYPE_OPTIONS),
            validator=colander.OneOf([s[0] for s in TYPE_OPTIONS]),
            missing="both",
            default="both",
        ),
    )
    schema.insert(
        0,
        supplier_filter_node_factory(
            name="supplier_id",
            is_global=True,
        ),
    )
    schema.insert(
        0,
        follower_filter_node_factory(
            name="follower_id",
            title="Accompagnateur",
        ),
    )
    schema.insert(0, company_filter_node_factory(name="company_id", title="Enseigne"))
    return schema
