"""
Admin view for balance sheet measures related settings
"""

import logging
import os
import datetime

from sqlalchemy import asc

from caerp.forms.admin import get_config_schema
from caerp.views.admin.accounting import (
    AccountingIndexView,
    ACCOUNTING_URL,
)
from caerp.models.accounting.balance_sheet_measures import (
    ActiveBalanceSheetMeasureType,
    PassiveBalanceSheetMeasureType,
    BalanceSheetMeasureGrid,
)

from caerp.utils.widgets import (
    POSTButton,
    Link,
)

from caerp.views.admin.tools import (
    AdminCrudListView,
    BaseConfigView,
    BaseAdminIndexView,
    BaseAdminAddView,
    BaseAdminDisableView,
)
from caerp.views.admin.accounting.income_statement_measures import (
    CategoryListView as IncomeStatementCategoryListView,
    CategoryAddView as IncomeStatementCategoryAddView,
    CategoryEditView as IncomeStatementCategoryEditView,
    CategoryDisableView as IncomeStatementCategoryDisableView,
    CategoryDeleteView as IncomeStatementCategoryDeleteView,
    TypeListIndexView as IncomeStatementTypeListIndexView,
    MeasureTypeListView as IncomeStatementMeasureTypeListView,
    MeasureTypeAddView as IncomeStatementMeasureTypeAddView,
    MeasureTypeEditView as IncomeStatementMeasureTypeEditView,
    MeasureDisableView as IncomeStatementMeasureDisableView,
    MeasureDeleteView as IncomeStatementMeasureDeleteView,
    move_view,
)

logger = logging.getLogger(__name__)


BASE_URL = os.path.join(ACCOUNTING_URL, "balance_sheet_measures")

ACTIVE_TYPE_LIST_INDEX_URL = BASE_URL + "/active_types"
ACTIVE_TYPE_LIST_ITEM_URL = ACTIVE_TYPE_LIST_INDEX_URL + "/{id}"

PASSIVE_TYPE_LIST_INDEX_URL = BASE_URL + "/passive_types"
PASSIVE_TYPE_LIST_ITEM_URL = PASSIVE_TYPE_LIST_INDEX_URL + "/{id}"


class BalanceSheetMeasureIndexView(BaseAdminIndexView):
    title = "Bilan comptable"
    description = (
        "Paramétrer l'état de gestion « Bilan » visible par les entrepreneurs."
    )
    route_name = BASE_URL


class ActiveMeasureTypeListView(IncomeStatementMeasureTypeListView):
    factory = ActiveBalanceSheetMeasureType
    category_class = None
    route_name = ACTIVE_TYPE_LIST_INDEX_URL
    item_route_name = ACTIVE_TYPE_LIST_ITEM_URL
    item_label = " actif du bilan"
    title = "Paramétrages des comptes de l'Actif"

    def more_template_vars(self, result):
        """
        Hook allowing to add datas to the templating context
        """
        result[
            "help_msg"
        ] = """Les définitions ci-dessous indiquent quelles
        écritures sont utilisées pour le calcul des indicateurs du bilan des
        entrepreneurs.<br />
        Les indicateurs seront présentés dans l'ordre.<br />"""
        return result

    def get_actions(self, items):
        """
        Return the description of additionnal main actions buttons

        :rtype: list
        """
        yield Link(
            self.get_addurl() + "&is_total=1",
            "Ajouter un total",
            title="Ajouter un indicateur de type total qui sera mis en "
            "évidence dans l'interface",
            icon="plus-circle",
            css="btn",
        )

    def get_addurl(self):
        return self.request.route_path(self.route_name) + "?action=add"


class ActiveMeasureTypeAddView(IncomeStatementMeasureTypeAddView):
    title = "Ajouter"
    route_name = ACTIVE_TYPE_LIST_INDEX_URL
    _schema = None
    factory = ActiveBalanceSheetMeasureType
    has_category = False


class ActiveMeasureTypeEditView(IncomeStatementMeasureTypeEditView):
    route_name = ACTIVE_TYPE_LIST_ITEM_URL
    _schema = None
    factory = ActiveBalanceSheetMeasureType


class ActiveMeasureDisableView(IncomeStatementMeasureDisableView):
    route_name = ACTIVE_TYPE_LIST_ITEM_URL
    factory = ActiveBalanceSheetMeasureType


class ActiveMeasureDeleteView(IncomeStatementMeasureDeleteView):
    route_name = ACTIVE_TYPE_LIST_ITEM_URL
    factory = ActiveBalanceSheetMeasureType


class PassiveMeasureTypeListView(IncomeStatementMeasureTypeListView):
    factory = PassiveBalanceSheetMeasureType
    category_class = None
    route_name = PASSIVE_TYPE_LIST_INDEX_URL
    item_route_name = PASSIVE_TYPE_LIST_ITEM_URL
    item_label = " passif du bilan"
    title = "Paramétrages des comptes du Passif"

    def more_template_vars(self, result):
        """
        Hook allowing to add datas to the templating context
        """
        result[
            "help_msg"
        ] = """Les définitions ci-dessous indiquent quelles
        écritures sont utilisées pour le calcul des indicateurs du bilan des
        entrepreneurs.<br />
        Les indicateurs seront présentés dans l'ordre.<br />"""
        return result

    def get_actions(self, items):
        """
        Return the description of additionnal main actions buttons

        :rtype: list
        """
        yield Link(
            self.get_addurl() + "&is_total=1",
            "Ajouter un total",
            title="Ajouter un indicateur de type total qui sera mis en "
            "évidence dans l'interface",
            icon="plus-circle",
            css="btn",
        )

    def get_addurl(self):
        return self.request.route_path(self.route_name) + "?action=add"


class PassiveMeasureTypeAddView(IncomeStatementMeasureTypeAddView):
    title = "Ajouter"
    route_name = PASSIVE_TYPE_LIST_INDEX_URL
    _schema = None
    factory = PassiveBalanceSheetMeasureType
    has_category = False


class PassiveMeasureTypeEditView(IncomeStatementMeasureTypeEditView):
    route_name = PASSIVE_TYPE_LIST_ITEM_URL
    _schema = None
    factory = PassiveBalanceSheetMeasureType


class PassiveMeasureDisableView(IncomeStatementMeasureDisableView):
    route_name = PASSIVE_TYPE_LIST_ITEM_URL
    factory = PassiveBalanceSheetMeasureType


class PassiveMeasureDeleteView(IncomeStatementMeasureDeleteView):
    route_name = PASSIVE_TYPE_LIST_ITEM_URL
    factory = PassiveBalanceSheetMeasureType


def add_routes(config):
    """
    Add routes related to this module
    """
    config.add_route(BASE_URL, BASE_URL)
    config.add_route(ACTIVE_TYPE_LIST_INDEX_URL, ACTIVE_TYPE_LIST_INDEX_URL)
    config.add_route(PASSIVE_TYPE_LIST_INDEX_URL, PASSIVE_TYPE_LIST_INDEX_URL)

    config.add_route(
        ACTIVE_TYPE_LIST_ITEM_URL,
        ACTIVE_TYPE_LIST_ITEM_URL,
        traverse="/active_balance_sheet_measure_types/{id}",
    )
    config.add_route(
        PASSIVE_TYPE_LIST_ITEM_URL,
        PASSIVE_TYPE_LIST_ITEM_URL,
        traverse="/passive_balance_sheet_measure_types/{id}",
    )


def add_views(config):
    """
    Add views defined in this module
    """
    config.add_admin_view(
        BalanceSheetMeasureIndexView,
        parent=AccountingIndexView,
    )
    # Active
    config.add_admin_view(
        move_view,
        route_name=ACTIVE_TYPE_LIST_ITEM_URL,
        request_param="action=move",
    )
    config.add_admin_view(
        ActiveMeasureTypeListView,
        parent=BalanceSheetMeasureIndexView,
        renderer="admin/crud_list.mako",
    )
    config.add_admin_view(
        ActiveMeasureTypeAddView,
        parent=ActiveMeasureTypeListView,
        renderer="admin/crud_add_edit.mako",
        request_param="action=add",
        permission="admin",
    )
    config.add_admin_view(
        ActiveMeasureTypeEditView,
        parent=ActiveMeasureTypeListView,
        renderer="admin/crud_add_edit.mako",
    )
    config.add_admin_view(
        ActiveMeasureDisableView,
        parent=ActiveMeasureTypeListView,
        request_param="action=disable",
    )
    config.add_admin_view(
        ActiveMeasureDeleteView,
        parent=ActiveMeasureTypeListView,
        request_param="action=delete",
    )
    # Passive
    config.add_admin_view(
        move_view,
        route_name=PASSIVE_TYPE_LIST_ITEM_URL,
        request_param="action=move",
    )
    config.add_admin_view(
        PassiveMeasureTypeListView,
        parent=BalanceSheetMeasureIndexView,
        renderer="admin/crud_list.mako",
    )
    config.add_admin_view(
        PassiveMeasureTypeAddView,
        parent=PassiveMeasureTypeListView,
        renderer="admin/crud_add_edit.mako",
        request_param="action=add",
        permission="admin",
    )
    config.add_admin_view(
        PassiveMeasureTypeEditView,
        parent=PassiveMeasureTypeListView,
        renderer="admin/crud_add_edit.mako",
    )
    config.add_admin_view(
        PassiveMeasureDisableView,
        parent=PassiveMeasureTypeListView,
        request_param="action=disable",
    )
    config.add_admin_view(
        PassiveMeasureDeleteView,
        parent=PassiveMeasureTypeListView,
        request_param="action=delete",
    )


def includeme(config):
    add_routes(config)
    add_views(config)
