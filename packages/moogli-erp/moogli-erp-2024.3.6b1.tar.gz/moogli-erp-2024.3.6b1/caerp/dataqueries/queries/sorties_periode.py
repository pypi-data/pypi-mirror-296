import logging

from caerp_base.models.base import DBSESSION
from caerp.models.user.utils import (
    get_userdatas_entry_date,
    get_user_analytical_accounts,
)
from caerp.dataqueries.base import BaseDataQuery
from caerp.utils.dataqueries import dataquery_class


logger = logging.getLogger(__name__)


@dataquery_class()
class ExitQuery(BaseDataQuery):
    name = "sorties_periode"
    label = "Liste des sorties sur une période"
    description = """
    Liste de tous les porteurs de projets ayant une étape de parcours de type "Sortie CAE" sur la période choisie.
    """

    def default_dates(self):
        self.start_date = self.date_tools.year_start()
        self.end_date = self.date_tools.year_end()

    def headers(self):
        headers = [
            "Identifiant MoOGLi",
            "Code(s) analytique(s)",
            "Civilité",
            "Nom",
            "Prénom",
            "Antenne de rattachement",
            "Date d'entrée dans la CAE",
            "Date de sortie",
            "Type de sortie",
            "Motif de sortie",
        ]
        return headers

    def data(self):
        from caerp.models.career_path import CareerPath

        data = []

        exits = (
            DBSESSION()
            .query(CareerPath)
            .filter(CareerPath.stage_type == "exit")
            .filter(CareerPath.start_date.between(self.start_date, self.end_date))
            .order_by(CareerPath.start_date)
            .all()
        )
        for e in exits:
            if not e.userdatas:
                logger.warn(f"Career path without userdatas (id={e.id})")
                continue
            u = e.userdatas
            exit_data = [
                u.user_id,
                get_user_analytical_accounts(u.user_id),
                u.coordonnees_civilite,
                u.coordonnees_lastname,
                u.coordonnees_firstname,
                u.situation_antenne.label if u.situation_antenne else "",
                self.date_tools.format_date(get_userdatas_entry_date(u.id)),
                self.date_tools.format_date(e.start_date),
                e.type_sortie.label if e.type_sortie else "",
                e.motif_sortie.label if e.motif_sortie else "",
            ]
            data.append(exit_data)
        return data
