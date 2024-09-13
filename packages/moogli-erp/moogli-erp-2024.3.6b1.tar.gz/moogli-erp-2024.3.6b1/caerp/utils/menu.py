from caerp.utils.html import (
    strip_html_tags,
)
from caerp.utils.sys_environment import egg_name
from webhelpers2.html import HTML


class BaseMenuElement:
    """
    Base Class for menu items

    Allows properties to be deferred (computed on each request)

    Permissions :

        :attr permission: The permission required to get this item displayed
        or a callable that will be called to get the responses
        :attr not_permission: The permission the user should not have to get
        this item displayed
    """

    def __init__(self, *args, **kw):
        self.bind_params = {}

    def bind(self, **kw):
        self.bind_params = kw

    def _is_deferred_property(self, propname):
        prop = getattr(self, propname, None)
        return callable(prop)

    def _get_deferred_property(self, propname, **params):
        """
        Get the property propname of the given object or call the callabl with
        the params if needed

        :param str propname: The name of the attribute
        :param dict params: The parameters
        :return: The associated property
        """
        if not params:
            params = self.bind_params
        prop = getattr(self, propname, None)
        if callable(prop):
            return prop(self, params)
        else:
            return prop

    def allowed(self, request, context=None):
        """
        Test if the end user should have access to this item

        :param obj request: The pyramid request object
        :param obj context: The alternative context on which we check the
        permission
        """
        result = True

        not_permission = self._get_deferred_property("not_permission")
        if not_permission is not None:
            result = not request.has_permission(not_permission, context=context)

        permission = self._get_deferred_property("permission")
        if self._is_deferred_property("permission"):
            # The permission has been computed by the get_deferred_property
            # call
            result = permission
        elif permission is not None:
            result = request.has_permission(permission, context=context)
        return result


class MenuItem(BaseMenuElement):
    __type__ = "item"
    """
    Une entrée de menu

    name

        Name of the entry used in the html code

    route_name

        Name of the route this entry is pointing on

    icon

        Name of the icon to display.

    label

        The label to display in the UI, if a callable is provided, it
        will be called with the menu's bind parameters

    title

        The title shown to the end user when he hovers the menu item

    perm

        If a string is provided, the user should have the associated permission
        on the current context to view this menu entry
        If a callable is provided, it will be called with the request
        as first argument then with the menu's bind parameters

    other_route_name

       Here you can specify other routes for which the menu entry can show
       itself as selected
    """

    def __init__(
        self,
        name,
        route_name,
        icon,
        label,
        title=None,
        perm=None,
        other_route_name=None,
        anchor="",
        **kw,
    ):
        BaseMenuElement.__init__(self, **kw)
        self.name = name

        if title is None:
            self.title = label
        else:
            self.title = title

        self.icon = icon
        self.label = label
        self.route_name = route_name
        self.other_route_name = other_route_name
        self.perm = perm
        self.anchor = anchor

    def url(self, context, request):
        return request.route_path(self.route_name, id=context.id) + self.anchor

    def enabled(self, context, request):
        return True

    def visible(self, context, request):
        return True

    def selected(self, context, request):
        if request.matched_route.name == self.route_name:
            return True
        if request.matched_route.name == self.other_route_name:
            return True
        return False

    def has_permission(self, context, request, **bind_params):
        if self.perm is not None:
            if callable(self.perm):
                if request not in bind_params:
                    bind_params["request"] = request
                return self.perm(self, bind_params)
            else:
                return request.has_permission(self.perm)
        return True

    def get_label(self, **params):
        return self._get_deferred_property("label", **params)

    def get_title(self, **params):
        return strip_html_tags(self._get_deferred_property("title", **params))


class MenuDropdown:
    """
    Dropdown menu
    icon
        An icon
    label
        A label (will be used as title on smaller viewports
    title
        The title shown on hovering the menu entry
    default_route
        If the menu is disabled, a link to that route will be provided instead
    """

    __type__ = "dropdown"

    def __init__(self, name, icon, label, title=None, default_route=None, perm=None):
        self.name = name
        if title is None:
            self.title = label
        else:
            self.title = title

        self.icon = icon
        self.label = label
        self.items = []
        self.default_route = default_route
        self.perm = perm

    def add_item(
        self,
        name,
        route_name,
        icon,
        label,
        title=None,
        perm=None,
        other_route_name=None,
    ):
        self.items.append(
            MenuItem(
                name,
                route_name,
                icon,
                label,
                title,
                perm=perm,
                other_route_name=other_route_name,
            )
        )

    def enabled(self, context, request):
        return True

    def url(self, context, request):
        if self.default_route:
            return request.route_path(self.default_route, id=context.id)

    def selected(self, context, request):
        res = False
        for item in self.items:
            if item.selected(context, request):
                res = True
                break
        return res

    def has_permission(self, context, request, **bind_params):
        if self.perm is not None:
            if callable(self.perm):
                if request not in bind_params:
                    bind_params["request"] = request
                return self.perm(self, bind_params)
            else:
                return request.has_permission(self.perm)
        return True

    def get_label(self, **params):
        if callable(self.label):
            return self.label(self, params)
        else:
            return self.label


class AttrMenuItem(MenuItem):
    """
    A menu item that is condionnaly active regarding a model's attribute

    hidden_attribute

        The context's attribute used to check if the menu should be shown or
        not (not shown if the attribute is None)

    disable_attribute

        The context's attribute used to check if the menu should be disabled
        (disabled if attribute is None)

    perm_context_attribute

        The current context's attribute used as context for the permission
        check


        E.g: if the context is a User and perm_context_attribute is
        "userdatas", we will chek the menu permission regarding the related
        UserDatas instance
    """

    def __init__(self, *args, **kw):
        self.hidden_attribute = kw.pop("hidden_attribute", None)
        self.disable_attribute = kw.pop("disable_attribute", None)
        self.perm_context_attribute = kw.pop("perm_context_attribute", None)
        MenuItem.__init__(self, **kw)

    def enabled(self, context, request):
        if self.disable_attribute is None:
            return True
        return getattr(context, self.disable_attribute, None) not in (None, [])

    def visible(self, context, request):
        if self.hidden_attribute is None:
            return True
        return getattr(context, self.hidden_attribute, None) is not None

    def has_permission(self, context, request, **bind_params):
        related = context
        if self.perm_context_attribute is not None:
            related = getattr(context, self.perm_context_attribute, None)

        if self.perm is not None and related is not None:
            return MenuItem.has_permission(self, context, request, **bind_params)
        return True


class AttrMenuDropdown(MenuDropdown):
    def __init__(self, *args, **kw):
        self.hidden_attribute = kw.pop("hidden_attribute", None)
        self.disable_attribute = kw.pop("disable_attribute", None)
        MenuDropdown.__init__(self, **kw)

    def enabled(self, context, request):
        if self.disable_attribute is None:
            return True
        return getattr(context, self.disable_attribute, None) is not None

    def visible(self, context, request):
        if self.hidden_attribute is None:
            return True
        return getattr(context, self.hidden_attribute, None) is not None


class Menu(BaseMenuElement):
    def __init__(self, name, **kw):
        BaseMenuElement.__init__(self)
        self.name = name
        self.items = []
        self.current = None

    def set_current(self, current):
        self.current = current

    def add(self, item):
        self.items.append(item)

    def add_before(self, name, new_item):
        """
        Add an item before the item named name
        """
        for index, item in enumerate(self.items[:]):
            if item.name == name:
                self.items.insert(index, new_item)
                return
        raise KeyError("Unknown node : %s" % name)

    def add_after(self, name, new_item):
        """
        Add an item after the item named name
        """
        for index, item in enumerate(self.items[:]):
            if item.name == name:
                self.items.insert(index + 1, new_item)
                return
        raise KeyError("Unknown node : %s" % name)

    def remove(self, name):
        for index, item in enumerate(self.items[:]):
            if item.name == name:
                self.items.pop(index)
                return
        raise KeyError("Unknown node : %s" % name)


class BaseAppMenuContainer(BaseMenuElement):
    def __init__(self, **kw):
        BaseMenuElement.__init__(self, **kw)
        self._items = []

    def add(self, item, parent_node=None):
        """
        Add an item in the menu registry
        """
        if parent_node is None:
            if item.order == -1:  # Order not specified
                item.order = len(self._items)
            self._items.append(item)
        else:
            matched = False
            for registered_item in self._items:
                if registered_item.name == parent_node:
                    registered_item.add(item)
                    matched = True
                    break
            if not matched:
                raise Exception("Unknown menu parent node {}".format(parent_node))

    @property
    def items(self):
        self._items.sort(key=lambda i: i.order)
        return self._items

    def find(self, name):
        result = None
        for item in self.items:
            if item.name == name:
                result = item
                break
        return result

    def remove(self, item):
        self._items.remove(item)

    def pop(self, index):
        item = self.items[index]
        self.remove(item)
        return item


class HtmlAppMenuItem(BaseMenuElement):
    """
    A static html item that's used to carry html generated code
    {'html': the html code}
    """

    __type__ = "static"

    def __init__(self, **kw):
        BaseMenuElement.__init__(self, **kw)
        self.html = kw["html"]
        if self.html[:3] != "<li":
            self.html = HTML.li(self.html)
        self.order = kw.get("order", -1)

    def build(self, *args, **kwargs):
        result = dict(
            html=self.html,
            __type__=self.__type__,
            order=self.order,
        )
        return result


class AppMenuItem(BaseMenuElement):
    """
    label
    icon
    route_name
    id_key (one of user_id/company_id)
    route_prefixes route prefix that will enable the item
    permission
    not_permission
    """

    __type__ = "item"

    def __init__(self, **kw):
        BaseMenuElement.__init__(self, **kw)
        self.name = kw.get("name")
        self.label = kw["label"]
        self.route_name = kw.get("route_name")
        self.route_id_key = kw.get("route_id_key")
        self.permission = kw.get("permission")
        self.href = kw.get("href")
        self.icon = kw.get("icon")
        self.routes_prefixes = kw.get("routes_prefixes", [])
        self.order = kw.get("order", -1)
        self._query_params = kw.get("route_query_params", {})

    def _href_match(self, request, href):
        return href == request.current_route_path(_query={})

    def _route_match(self, request):
        for route in self.routes_prefixes:
            if request.matched_route.name.startswith(route):
                return True
        return False

    def selected(self, request, href):
        return self._href_match(request, href) or self._route_match(request)

    def _get_href(self, request, **params):
        """
        Build the url
        """
        url = self.href
        if not url:
            route_name = self._get_deferred_property("route_name")
            id_key = self._get_deferred_property("route_id_key")
            if id_key:
                url = request.route_path(
                    route_name,
                    id=params[id_key],
                    _query=self._query_params,
                )
            else:
                url = request.route_path(route_name, _query=self._query_params)
        return url

    def build(self, request, context=None, **params):
        """
        Build a menuitem for the final rendering
        1- bind
        2- build

        :rtype: dict
        """
        self.bind(request=request, **params)
        result = {}
        if self.allowed(request, context):
            result["href"] = self._get_href(request, **params)
            result["icon"] = self.icon
            result["label"] = self._get_deferred_property("label")
            result["selected"] = self.selected(request, result["href"])
            result["__type__"] = self.__type__
        return result


class AppMenu(BaseAppMenuContainer):
    __type__ = "menu"

    def build(self, request, context=None, **params):
        self.bind(request=request, **params)
        result = None
        if self.allowed(request, context):
            result = {}
            result["__type__"] = self.__type__

            for item in self.items:
                built_item = item.build(request, context, **params)
                if built_item:
                    result.setdefault("items", []).append(built_item)

            if "items" not in result:
                result = {}
        return result


class AppMenuDropDown(AppMenu):
    __type__ = "dropdown"

    def __init__(self, **kw):
        AppMenu.__init__(self, **kw)
        self.name = kw["name"]
        self.label = kw["label"]
        self.icon = kw.get("icon")
        self.permission = kw.get("permission")
        self.order = kw.get("order", -1)

    def build(self, request, context=None, **params):
        result = AppMenu.build(self, request, context, **params)
        if result:
            result["label"] = self.label
            result["icon"] = self.icon
        return result


CAERP_FORUM_LINK = HTML.tag(
    "a",
    href="https://forum.endi.coop",
    c="Forum des utilisateurs d’MoOGLi",
    target="_blank",
    title="Ouvrir le forum des utilisateurs d’MoOGLi dans une nouvelle fenêtre",
)
CAERP_DOC_LINK = HTML.tag(
    "a",
    href="https://doc.endi.coop",
    c="Documentation",
    target="_blank",
    title="Ouvrir la documentation d’MoOGLi dans une nouvelle fenêtre",
)


def add_help_menu(result):
    result.add(AppMenuDropDown(name="help", label="Aide"))
    if egg_name == "endi":
        result.add(HtmlAppMenuItem(html=CAERP_FORUM_LINK), "help")
        result.add(HtmlAppMenuItem(html=CAERP_DOC_LINK), "help")

    result.add(AppMenuItem(href="/release_notes", label="Notes de version"), "help")
    return result


def build_admin_menu_registry():
    """
    Build the manager menu structure that will be filled by the different
    modules
    """
    result = AppMenu()
    result.add(AppMenuItem(href="/manage", label="Accueil", icon=""))
    result.add(AppMenuItem(label="Configuration", permission="admin", href="/admin"))
    result.add(AppMenuDropDown(name="sale", label="Gestion commerciale"))
    result.add(
        AppMenuDropDown(
            name="accounting",
            label="Comptabilité",
            permission="admin_treasury",
        )
    )
    result.add(AppMenuDropDown(name="accompagnement", label="Accompagnement"))
    result.add(AppMenuDropDown(name="userdata", label="Gestion sociale"))
    result.add(
        AppMenuDropDown(
            name="training", label="Formations", permission="admin.training"
        )
    )
    result.add(AppMenuDropDown(name="management", label="Suivi de gestion"))
    result.add(AppMenuItem(href="/dataqueries", label="Requêtes statistiques", icon=""))
    result.add(
        AppMenuDropDown(
            name="validation", label="Centre de validation", permission="admin.invoices"
        )
    )

    result.add(AppMenuDropDown(name="annuaire", label="Annuaires"))
    result.add(AppMenuItem(label="Utilisateurs", href="/users"), "annuaire")
    result.add(AppMenuItem(label="Enseignes", href="/companies"), "annuaire")
    result = add_help_menu(result)

    return result


def build_company_menu_registry():
    """
    Build the menu structure for the Company menu.
    This Structure will be filled in the different modules

    :returns: A AppMenu instance
    """
    from caerp.views.company.routes import (
        DASHBOARD_ROUTE,
        ITEM_ROUTE as COMPANY_ITEM_ROUTE,
    )

    result = AppMenu()
    result.add(
        AppMenuItem(
            route_name=DASHBOARD_ROUTE,
            route_id_key="company_id",
            label="Accueil",
            icon="",
            name="dashboard",
        )
    )
    result.add(AppMenuDropDown(name="sale", label="Vente"))
    result.add(AppMenuDropDown(name="supply", label="Achat"))
    result.add(AppMenuDropDown(name="accounting", label="États de gestion"))
    result.add(AppMenuDropDown(name="document", label="Documents"))
    result.add(AppMenuDropDown(name="accompagnement", label="Accompagnement"))
    result.add(AppMenuDropDown(name="worktools", label="Outils métier"))

    def deferred_label(menu, kw):
        if kw["submenu"]:
            return "Fiche de l'enseigne"
        else:
            return "Mon enseigne"

    result.add(
        AppMenuItem(
            label=deferred_label,
            route_name=COMPANY_ITEM_ROUTE,
            route_id_key="company_id",
            name="company",
        )
    )

    def deferred_submenu_perm(menu, kw):
        """
        Return True if the built menu will be a submenu
        """
        return not kw["submenu"]

    result.add(
        AppMenuItem(
            label="Annuaire",
            name="users",
            href="/users",
            permission=deferred_submenu_perm,
        )
    )
    result = add_help_menu(result)
    return result


def build_user_menu_registry():
    """
    Build a AppMenu that will be attached to the global registry
    Can then be used to add menu entries, module after module
    """
    menu = AppMenu()
    menu.add(
        AppMenuItem(
            label="Mon compte",
            route_name="/users/{id}",
            route_id_key="user_id",
        )
    )
    menu.add(
        AppMenuItem(
            label="Déconnexion",
            icon="times",
            href="/logout",
        )
    )
    return menu


def add_admin_menu(config, **params):
    item = AppMenuItem(**params)
    parent_node = params.pop("parent", None)
    config.registry.admin_menu.add(item, parent_node)


def add_company_menu(config, **params):
    item = AppMenuItem(**params)
    parent_node = params.pop("parent", None)
    config.registry.company_menu.add(item, parent_node)


def add_user_menu(config, **params):
    item = AppMenuItem(**params)
    config.registry.user_menu.add(item)


def add_menu_item_directive(config):
    """

    config.add_menu(item, 'admin', 'accompagnement'
    """
    config.registry.admin_menu = build_admin_menu_registry()
    config.registry.company_menu = build_company_menu_registry()
    config.registry.user_menu = build_user_menu_registry()
    config.add_directive("add_admin_menu", add_admin_menu)
    config.add_directive("add_company_menu", add_company_menu)
    config.add_directive("add_user_menu", add_user_menu)


def includeme(config):
    config.include(add_menu_item_directive)
