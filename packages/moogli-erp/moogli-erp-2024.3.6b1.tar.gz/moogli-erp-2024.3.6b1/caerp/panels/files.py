from caerp.utils.widgets import (
    Link,
    POSTButton,
)
from caerp.models.user.user import User
from caerp.models.user.userdatas import UserDatas
from caerp.views.files.routes import FILE_ITEM


def stream_actions(request, item):
    """
    Collect actions available for the given item
    """
    file_edit_route_path = request.route_path(FILE_ITEM, id=item.id)
    if isinstance(request.context, User) or isinstance(request.context, UserDatas):
        file_edit_route_path = request.route_path(
            "userdatas_file", id=request.context.id, id2=item.id
        )

    if request.has_permission("edit.file", item):
        yield Link(file_edit_route_path, "Voir ou modifier", icon="pen", css="icon")
    if request.has_permission("view.file", item):
        yield Link(
            request.route_path(FILE_ITEM, id=item.id, _query=dict(action="download")),
            "Télécharger",
            icon="download",
            css="icon",
        )

    if request.has_permission("delete.file", item):
        yield POSTButton(
            request.route_path(FILE_ITEM, id=item.id, _query=dict(action="delete")),
            "Supprimer",
            confirm="Êtes-vous sûr de vouloir définitivement supprimer " "ce fichier ?",
            icon="trash-alt",
            css="icon negative",
        )


def parent_label(node):
    """
    Render a label for the given node

    :param obj node: :class:`caerp.models.node.Node` instance
    :returns: A label for filetable display
    """
    return "{0} : {1}".format(
        node.parent.type_label,
        node.parent.name,
    )


def filetable_panel(
    context,
    request,
    add_url,
    files,
    add_perm="add.file",
    help_message=None,
    show_parent=False,
):
    """
    render a table listing files

    files should be loaded with the following columns included :

        description
        updated_at
        id
        parent.id
        parent.name
        parent.type_


    :param obj context: The context for which we display the files
    :param str add_url: The url for adding elements
    :param list files: A list of :class:`caerp.models.files.File`
    :param str add_perm: The permission required to add a file
    :param str help_message: An optionnal help message
    :param bool show_parent: Should a column show the parent ?
    :returns: dict
    """
    return dict(
        files=files,
        add_url=add_url,
        stream_actions=stream_actions,
        add_perm=add_perm,
        help_message=help_message,
        parent_label=parent_label,
        show_parent=show_parent,
    )


def includeme(config):
    config.add_panel(
        filetable_panel,
        "filetable",
        renderer="panels/filetable.mako",
    )
