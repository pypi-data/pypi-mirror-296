from caerp.utils.widgets import POSTButton, Link

from caerp.resources import estimation_signed_status_js

from caerp.views.task.utils import get_task_url, task_pdf_link
from caerp.views.task.layout import TaskLayout, get_task_menu
from .routes import (
    ESTIMATION_ITEM_FILES_ROUTE,
    ESTIMATION_ITEM_GENERAL_ROUTE,
    ESTIMATION_ITEM_PREVIEW_ROUTE,
)


def estimation_menu(layout_class):
    menu = get_task_menu(
        ESTIMATION_ITEM_GENERAL_ROUTE,
        ESTIMATION_ITEM_PREVIEW_ROUTE,
        ESTIMATION_ITEM_FILES_ROUTE,
    )
    return menu


class EstimationLayout(TaskLayout):
    menu_factory = estimation_menu

    @property
    def title(self):
        internal = ""
        if self.context.internal:
            internal = "interne "
        return (
            f"Devis {internal}N<span class='screen-reader-text'>umér</span>"
            f"<sup>o</sup>{self.context.internal_number} avec le client "
            f"{self.context.customer.label}"
        )

    def stream_main_actions(self):
        has_invoices = len(self.context.invoices) > 0

        if self.request.has_permission("geninv.estimation"):
            params = {
                "url": get_task_url(self.request, suffix="/geninv"),
                "label": "Facturer",
                "icon": "file-invoice-euro",
                "title": "Transformer ce devis en facture",
                "css": "btn icon btn-primary",
            }
            if has_invoices or self.context.geninv:
                params["label"] = "Re-facturer"
                params["title"] = "Transformer à nouveau ce devis en facture"
                params["icon"] = "file-redo"

            yield POSTButton(**params)
        elif self.request.has_permission("genbusiness.estimation"):
            if self.context.business_id:
                yield Link(
                    self.request.route_path(
                        "/businesses/{id}", id=self.context.business_id
                    ),
                    label="Voir l'affaire",
                    title="Voir l’affaire : {}".format(self.context.business.name),
                    icon="folder",
                )
            else:
                yield POSTButton(
                    get_task_url(self.request, suffix="/genbusiness"),
                    "Générer une affaire",
                    icon="file-invoice-euro",
                    css="btn btn-primary icon_only_mobile",
                    title=(
                        "Générer une affaire ({}) au sein de laquelle facturer le devis".format(
                            self.context.business_type.label
                        )
                    ),
                )

        if self.request.has_permission("draft.estimation"):
            yield POSTButton(
                get_task_url(self.request, suffix="/set_draft"),
                label="Repasser en brouillon",
                icon="pen",
                css="btn btn-primary icon_only_mobile",
                title="Repasser ce devis en brouillon pour pouvoir le modifier",
            )

        if not has_invoices and not self.context.internal:
            yield Link(
                get_task_url(self.request, suffix="/attach_invoices"),
                'Rattacher<span class="no_tablet">&nbsp;à des factures</span>',
                title="Rattacher ce devis à des factures",
                icon="link",
                css="btn icon_only_mobile",
            )

        if self.request.has_permission("gen_supplier_order.estimation"):
            yield POSTButton(
                get_task_url(self.request, suffix="/gen_supplier_order"),
                "Commande fournisseur",
                icon="plus",
                title=(
                    "Générer la commande fournisseur dans l'espace de "
                    "l'enseigne {}".format(self.context.customer.label)
                ),
            )

    def stream_more_actions(self):
        if self.request.has_permission("duplicate.estimation"):
            yield Link(
                get_task_url(self.request, suffix="/duplicate"),
                label="",
                title="Dupliquer ce devis",
                icon="copy",
            )
        yield Link(
            get_task_url(self.request, suffix="/set_metadatas"),
            "",
            title="Déplacer ou renommer ce devis",
            icon="folder-move",
        )
        yield task_pdf_link(self.request, "ce devis")


def includeme(config):
    config.add_layout(
        EstimationLayout,
        template="caerp:templates/tasks/estimation/layout.mako",
        name="estimation",
    )
