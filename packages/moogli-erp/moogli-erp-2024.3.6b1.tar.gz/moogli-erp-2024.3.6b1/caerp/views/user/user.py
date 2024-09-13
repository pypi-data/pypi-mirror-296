"""
User Related views
"""
import logging

from pyramid.httpexceptions import HTTPFound
from sqlalchemy import or_

from caerp.models.user.user import User
from caerp.forms import (
    merge_session_with_post,
)
from caerp.forms.user.user import (
    get_add_edit_schema,
    get_edit_account_schema,
    get_edit_accounting_schema,
)
from caerp.views import (
    BaseFormView,
    DeleteView,
    BaseEditView,
)
from caerp.views.user.routes import (
    USER_URL,
    USER_ADD_URL,
    USER_ADD_MANAGER_URL,
    USER_ITEM_URL,
    USER_ACCOUNTING_URL,
    USER_MYACCOUNT_URL,
    USER_ITEM_EDIT_URL,
    USER_LOGIN_ADD_URL,
)
from caerp.views.user.tools import UserFormConfigState
from caerp.views.files.routes import FILE_PNG_ITEM


logger = logging.getLogger(__name__)


def user_view(context, request):
    """
    Collect datas for the user view
    """
    return dict(
        user=context,
        title="Compte utilisateur",
    )


def user_add_manager_entry_point(context, request):
    """
    Entry point for manager user add
    Prepare the form configuration

    The add process follows this stream :
        1- entry point
        2- user add form
        3- login add form
    """
    config = UserFormConfigState(request.session)
    config.set_defaults({"primary_group": "manager", "add_login": True})
    return HTTPFound(request.route_path(USER_ADD_URL))


class UserAddView(BaseFormView):
    """
    view handling user add, also check for existing similar accounts
    """

    title = "Ajouter un compte"
    schema = get_add_edit_schema()

    def __init__(self, *args, **kwargs):
        BaseFormView.__init__(self, *args, **kwargs)
        self.form_config = UserFormConfigState(self.session)

    def before(self, form):
        logger.debug(
            "In the login form, defaults {0}".format(self.form_config.get_defaults())
        )
        add_login = self.form_config.pop_default("add_login", False)
        if add_login:
            form.set_appstruct({"add_login": True})

    def query_homonym(self, lastname, email):
        """
        collect the accounts with same name or email

        :param str lastname: The lastname to check
        :param str email: the email to check
        :returns: The SQLAlchemy query object
        :rtype: obj
        """
        query = User.query().filter(
            or_(
                User.lastname == lastname,
                User.email == email,
            )
        )
        return query

    def _confirmation_form(self, query, appstruct, query_count):
        """
        Return datas used to display a confirmation form

        :param obj query: homonym SQLAlchemy query object
        :param dict appstruct: Preserved form datas
        :param int query_count: The number of homonyms
        :returns: template vars
        :rtype: dict
        """
        form = self._get_form()
        _query = self.request.GET.copy()
        _query["confirmation"] = "1"
        form.action = self.request.current_route_path(_query=_query)

        form.set_appstruct(appstruct)
        datas = dict(
            duplicate_accounts=query.all(),
            appstruct=appstruct,
            form=form.render(),
            confirm_form_id=form.formid,
            user_view_route=USER_ITEM_URL,
            back_url=self.request.route_path(USER_URL),
        )
        datas.update(self._more_template_vars())
        return datas

    def submit_success(self, appstruct):
        """
        Handle successfull form submission

        :param dict appstruct: The submitted datas
        """
        logger.debug("Adding a new user account")
        logger.debug(appstruct)

        confirmation = self.request.GET.get("confirmation", "0")
        lastname = appstruct["lastname"]
        email = appstruct["email"]

        if confirmation == "0":  # Check homonyms
            query = self.query_homonym(lastname, email)
            count = query.count()
            if count > 0:
                return self._confirmation_form(query, appstruct, count)

        add_login = appstruct.pop("add_login", False)

        model = self.schema.objectify(appstruct)

        self.dbsession.add(model)
        self.dbsession.flush()

        if add_login:
            redirect = self.request.route_path(
                USER_LOGIN_ADD_URL,
                id=model.id,
            )
        else:
            next_step = self.form_config.get_next_step()
            if next_step is not None:
                redirect = self.request.route_path(
                    next_step,
                    id=model.id,
                )
            else:
                redirect = self.request.route_path(
                    USER_ITEM_URL,
                    id=model.id,
                )
        logger.debug("Account with id {0} added".format(model.id))
        return HTTPFound(redirect)


class UserAccountingEditView(BaseEditView):
    schema = get_edit_accounting_schema()
    title = "Configuration des informations comptables"

    def redirect(self, appstruct):
        return HTTPFound(
            self.request.route_path(
                USER_ITEM_URL,
                id=self.context.id,
            )
        )


class UserAccountEditView(BaseEditView):
    """
    View allowing a end user to modify some of his account informations
    """

    schema = get_edit_account_schema()
    title = "Modifier mes informations"
    msg = "Vos modifications ont bien été enregistrées"

    def get_default_appstruct(self):
        appstruct = self.context.appstruct()
        file_id = appstruct.pop("photo_id", "")
        if file_id:
            appstruct["photo"] = {
                "uid": self.context.photo.name,
                "filename": self.context.photo.name,
                "preview_url": self.request.route_path(
                    FILE_PNG_ITEM,
                    id=file_id,
                ),
            }
        return appstruct

    def merge_appstruct(self, appstruct, model):
        model = merge_session_with_post(model, appstruct, remove_empty_values=False)
        return model

    def on_edit(self, appstruct, model):
        self.request.session.pop("substanced.tempstore")
        self.request.session.changed()

    def redirect(self, appstruct):
        return HTTPFound(
            self.request.route_path(
                USER_ITEM_URL,
                id=self.context.id,
            )
        )


class UserEditView(UserAccountEditView):
    schema = get_add_edit_schema(edit=True)
    title = "Modifier les informations de l'utilisateur"


class UserDeleteView(DeleteView):
    redirect_route = USER_URL


def includeme(config):
    """
    Add module related views
    """
    config.add_view(
        user_view,
        route_name=USER_ITEM_URL,
        permission="view.user",
        renderer="/user/user.mako",
        layout="user",
    )
    config.add_view(
        UserAccountingEditView,
        route_name=USER_ACCOUNTING_URL,
        permission="admin_treasury",
        renderer="caerp:templates/user/accounting.mako",
        layout="user",
    )

    config.add_view(
        UserAccountEditView,
        route_name=USER_MYACCOUNT_URL,
        permission="set_email.user",
        renderer="caerp:templates/base/formpage.mako",
        layout="default",
    )

    config.add_view(
        user_add_manager_entry_point,
        route_name=USER_ADD_MANAGER_URL,
        permission="add.user",
    )

    config.add_view(
        UserAddView,
        route_name=USER_URL,
        request_param="action=add",
        permission="add.user",
        renderer="/user/add.mako",
        layout="default",
    )
    config.add_view(
        UserAddView,
        route_name=USER_ADD_URL,
        permission="add.user",
        renderer="/user/add.mako",
        layout="default",
    )

    config.add_view(
        UserEditView,
        route_name=USER_ITEM_EDIT_URL,
        permission="edit.user",
        renderer="/user/edit.mako",
        layout="user",
    )

    config.add_view(
        UserDeleteView,
        route_name=USER_ITEM_URL,
        permission="delete.user",
        request_param="action=delete",
        request_method="POST",
        require_csrf=True,
    )
