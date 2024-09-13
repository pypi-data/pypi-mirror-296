import argparse
import logging
import json
import os
import base64
from pathlib import Path
import sys
from typing import (
    Callable,
    Union,
    TypeVar,
)
from pkg_resources import resource_filename

from pyramid.paster import bootstrap
from sqlalchemy.exc import NoResultFound

from caerp.scripts.utils import argparse_command
from caerp_base.models.base import DBSESSION
from caerp.forms.user.user import User
from caerp.forms.user.login import Login
from caerp.utils.datetimes import parse_datetime
from caerp.utils.notification import (
    AbstractNotification,
    notify,
)


PWD_LENGTH = 10


def get_pwd() -> str:
    """
    Return a random password
    """
    return base64.b64encode(os.urandom(PWD_LENGTH)).decode()


class AbstractCommand:
    """
    Docstring will be used as CLI doc
    """

    name = None

    @classmethod
    def add_arguments(cls, parser: argparse.ArgumentParser) -> None:
        """Adds arguments to the subcmd parser

        no-op if no special arguments is used for the subcmd

        :param parser: the sub-command parser already added to main CMD subparsers
        """
        return None

    @staticmethod
    def __call__(arguments: argparse.Namespace, env: dict):
        raise NotImplementedError


CommandClassType = TypeVar("CommandClassType", bound=AbstractCommand)


class UserAddcommand(AbstractCommand):
    """
    Add a user in the database
    """

    name = "useradd"

    @classmethod
    def add_arguments(cls, parser) -> None:
        parser.add_argument("--username", default="admin")
        parser.add_argument("--password", "--pwd", default=get_pwd)
        parser.add_argument("--firstname", default="Admin")
        parser.add_argument("--lastname", default="CAERP")
        parser.add_argument("--email", default="admin@example.com")
        parser.add_argument("--group", default=None)

    @staticmethod
    def __call__(arguments: argparse.Namespace, env):
        is_autogen_password = not isinstance(arguments.password, str)

        if is_autogen_password:
            # callable for default
            password = arguments.password()
        else:
            password = arguments.password

        logger = logging.getLogger(__name__)
        logger.debug("Adding a user {0}".format(arguments.username))

        login = Login(login=arguments.username)
        login.set_password(password)

        if arguments.group:
            try:
                login.groups.append(arguments.group)
            except NoResultFound:
                print(
                    (
                        """

    ERROR : group %s doesn't exist, have you launched the syncdb command :

        caerp-admin <fichier.ini> syncdb
                    """
                        % (arguments.group,)
                    )
                )
                return

        db = DBSESSION()
        db.add(login)
        db.flush()

        user = User(
            login=login,
            firstname=arguments.firstname,
            lastname=arguments.lastname,
            email=arguments.email,
        )
        db.add(user)
        db.flush()
        print(
            (
                """
        User Account created :
              ID        : {0.id}
              Login     : {0.login.login}
              Firstname : {0.firstname}
              Lastname  : {0.lastname}
              Email     : {0.email}
              Groups    : {0.login.groups}
              """.format(
                    user
                )
            )
        )

        if is_autogen_password:
            print(
                (
                    """
              Password  : {0}""".format(
                        password
                    )
                )
            )

        logger.debug("-> Done")
        return user


class TestMailCommand(AbstractCommand):
    """
    Test tool for mail sending
    """

    name = "testmail"

    @classmethod
    def add_arguments(cls, parser) -> None:
        parser.add_argument("--to", default="contact@endi.coop")

    @staticmethod
    def __call__(arguments: argparse.Namespace, env):
        from caerp_base.mail import send_mail

        request = env["request"]
        subject = "Test d'envoi de mail"
        body = """Il semble que le test d'envoi de mail a réussi.
        Ce test a été réalisé depuis le script caerp-admin

        Bonne et belle journée !!!"""

        send_mail(request, [arguments.to], body, subject)


class SyncdbCommand(AbstractCommand):
    """
    Populate the database with the initial datas
    """

    name = "syncdb"

    @classmethod
    def add_arguments(cls, parser) -> None:
        parser.add_argument("--pkg", default="caerp")

    @staticmethod
    def __call__(arguments, env):
        from caerp.models.populate import populate_database

        logger = logging.getLogger(__name__)

        populate_database()
        from caerp.scripts.caerp_migrate import (
            fetch_head_command,
            is_alembic_initialized,
        )

        # Do not fetch current head on an existing instance (risk of skipping migrations):
        if not is_alembic_initialized(arguments.pkg):
            logger.info(
                "Fetching current alembic head, skipping all migrations (new installation)"
            )
            fetch_head_command(arguments.pkg)


class ResizeHeadersCommand(AbstractCommand):
    """
    bulk resize company header files to limit pdf size
    """

    name = "resize_headers"

    @classmethod
    def add_arguments(cls, parser) -> None:
        parser.add_argument("--limit", default=None)
        parser.add_argument("--offset", default=None)

    @staticmethod
    def __call__(arguments: argparse.Namespace, env: dict):
        from sqlalchemy import distinct
        from caerp.models.files import File
        from caerp.models.company import Company
        from caerp.forms.company import HEADER_RESIZER

        session = DBSESSION()
        file_id_query = session.query(distinct(Company.header_id))
        if arguments.limit:
            file_id_query = file_id_query.limit(arguments.limit)
            if arguments.offset:
                file_id_query = file_id_query.offset(arguments.offset)

        header_ids = [i[0] for i in file_id_query]
        header_files = File.query().filter(File.id.in_(header_ids))
        for header_file in header_files:
            file_datas = header_file.data_obj
            if file_datas:
                print(("Resizing header with id : {}".format(header_file.id)))
                header_file.data = HEADER_RESIZER.complete(file_datas)
                session.merge(header_file)


class SendNotificationCommand(AbstractCommand):
    """
    envoie une notification à des utilisateurs
    TODO : envoie avec un délai (pas encore implémenté dans le script)
    """

    name = "notify"

    @classmethod
    def add_arguments(cls, parser) -> None:
        parser.add_argument(
            "-g",
            "--groups",
            dest="groups",
            nargs="+",
            required=False,
            help="Nom des groupes utilisateur",
        )
        parser.add_argument(
            "--uids",
            nargs="*",
            dest="uids",
            required=False,
            help="Identifiants du destinataire",
        )
        parser.add_argument(
            "-f",
            "--filename",
            dest="filename",
            required=False,
            help="Chemin vers un fichier json de version (caerp:release_notes.json)",
        )
        parser.add_argument("--title", required=False, help="titre de la notification")
        parser.add_argument("--body", required=False, help="Message")
        parser.add_argument(
            "-c",
            "--channel",
            dest="channel",
            required=False,
            help="Force le canal de communication (email, header_message, alert, "
            "message), Défaut: alert",
        )
        parser.add_argument(
            "--versions",
            dest="versions",
            required=False,
            nargs="+",
            help="Versions à inclure dans la notification (compatible uniquement "
            "si on utilise les release notes). Défaut: la dernière",
        )
        parser.add_argument(
            "-k",
            "--event-key",
            dest="event_key",
            required=False,
            default="message:system",
            help=(
                "Type d'évènement, doit correspondre à un des types prédéfinis par "
                "caerp ou un de ses plugins (voir models/populate). "
                "Défaut: 'message:system'"
            ),
        )
        parser.add_argument(
            "--from",
            dest="from_time",
            required=False,
            help="Date d'apparition de la notification (format 2023-12-05 12:00:00)",
        )
        parser.add_argument(
            "--until",
            dest="until_time",
            required=False,
            help="Date de fin d'apparition de la notification (format "
            "2023-12-05 12:00:00)",
        )

    def _validate_dest(self, arguments):
        groups = arguments.groups
        uids = arguments.uids
        if not uids and not groups:
            raise Exception("Il manque un destinataire (uids ou groups)")
        return groups, uids

    def _get_release_notes(self, file_content, versions):
        if not versions:
            return [file_content["release_notes"][0]]
        else:
            result = []
            for release_note in file_content["release_notes"]:
                if release_note["version"] in versions:
                    result.append(release_note)
            return result

    def _get_content_from_version_note(self, filename, request, versions):
        from caerp.utils.renderer import render_template

        resource = filename
        if ":" in filename:
            pkg_name, filename = filename.split(":")
            resource = resource_filename(pkg_name, filename)

        with open(resource, "r") as fbuf:
            data = json.load(fbuf)

        release_notes = self._get_release_notes(data, versions)
        if not release_notes:
            raise Exception(
                f"Aucune note de version trouvée pour les " f"versions {versions}"
            )

        template = "caerp:templates/notifications/release_note_alert.mako"
        tmpl_data = {
            "enhancements": [
                note
                for release_note in release_notes
                for note in release_note["changelog"]
                if note["category"] == "enhancement"
            ],
            "bugfixs": [
                note
                for release_note in release_notes
                for note in release_note["changelog"]
                if note["category"] == "bugfix"
            ],
        }
        if len(release_notes) == 1:
            title = f"Nouveautés de la version {release_notes[0]['version']}"
        else:
            title = f"Nouveautés des versions {', '.join(versions)}"
        body = render_template(template, tmpl_data, request=request)
        return title, body

    def _validate_content(self, arguments, request):
        title = arguments.title
        body = arguments.body
        filename = arguments.filename
        versions = arguments.versions
        if not (title and body) and not filename:
            raise Exception("Il manque un message à envoyer")
        if filename:
            if "release" in filename:
                title, body = self._get_content_from_version_note(
                    filename, request, versions
                )
            else:
                path = Path(filename)
                if not path.exists():
                    raise Exception(f"Fichier {filename} introuvable")
                with open(filename, "r") as fbuf:
                    body = fbuf.read()
        return title, body

    def _validate_channel(self, arguments):
        channel = arguments.channel
        event_key = arguments.event_key
        if not channel and not event_key:
            raise Exception("Il manque soit un channel soit une clé d'évènement")
        return channel, event_key

    def _validate_times(self, arguments):
        from_time = arguments.from_time
        until_time = arguments.until_time
        from_datetime = None
        if from_time:
            try:
                from_datetime = parse_datetime(from_time)
            except Exception:
                raise Exception("Erreur dans le format de la date de départ")
        if until_time:
            try:
                parse_datetime(until_time)
            except Exception:
                raise Exception("Erreur dans le format de la date de fin")
        return from_datetime, until_time

    def __call__(self, arguments: argparse.Namespace, env: dict):
        groups, uids = self._validate_dest(arguments)

        title, body = self._validate_content(arguments, env["request"])
        channel, event_key = self._validate_channel(arguments)
        from_datetime, until_time = self._validate_times(arguments)

        check_query = None
        if until_time:
            check_query = f"SELECT NOW() < '{until_time}'"

        notification = AbstractNotification(
            key=event_key,
            title=title,
            body=body,
            due_datetime=from_datetime,
            check_query=check_query,
        )
        notify(
            env["request"],
            notification,
            group_names=groups,
            user_ids=uids,
            force_channel=channel,
        )


class SetEnvCommand(AbstractCommand):
    """
    Change l'environnement de distribution de l'application

    Ex : caerp-admin development.ini setenv --env=endi
    """

    name = "setenv"

    @classmethod
    def add_arguments(cls, parser) -> None:
        parser.add_argument("--env", default="caerp")

    def __call__(self, arguments: argparse.Namespace, env: dict):
        import subprocess
        from distutils.dir_util import copy_tree

        AVAILABLE_ENVS = ["caerp", "endi", "moogli"]
        ENV_DIRECTORIES = [
            "css_sources",
            "caerp/static/favicons",
            "caerp/static/img",
            "caerp/static/svg",
        ]

        if arguments.env not in AVAILABLE_ENVS:
            print(
                f"ERREUR : L'environnement demandé n'existe pas.\n\n\
Choix disponibles : {AVAILABLE_ENVS}"
            )
            sys.exit(1)

        print(f"Bascule vers l'environnement '{arguments.env}'")
        for dir in ENV_DIRECTORIES:
            print(f" > Copie des fichiers depuis '{dir}/{arguments.env}' ...")
            copy_tree(f"{dir}/{arguments.env}", dir)
        print(" > Recompilation des fichiers CSS ...")
        subprocess.run(
            """
            cd css_sources
            boussole compile
            cd ..
            """,
            shell=True,
        )
        print(f"\n[ SUCCÈS ] L'environnement est maintenant '{arguments.env}' !\n")


class CaerpAdminCommandsRegistry:
    BASE_COMMANDS = [
        UserAddcommand,
        TestMailCommand,
        SyncdbCommand,
        ResizeHeadersCommand,
        SendNotificationCommand,
        SetEnvCommand,
    ]

    EXTRA_COMMANDS = []

    @classmethod
    def _get_all_commands(cls):
        return cls.EXTRA_COMMANDS + cls.BASE_COMMANDS

    @classmethod
    def add_function(cls, command_class: CommandClassType) -> None:
        cls.EXTRA_COMMANDS.append(command_class)

    @classmethod
    def get_command(cls, name: str) -> Union[Callable[[dict, dict], None], None]:
        """
        :param name: the command name
        :returns None if no known command is mentioned in arguments
        """
        for cmd in cls._get_all_commands():
            if cmd.name == name:
                return cmd()

    @classmethod
    def get_argument_parser(cls):
        parser = argparse.ArgumentParser(description="CAERP administration tool")
        parser.add_argument("config_uri")

        subparsers = parser.add_subparsers(dest="subcommand", required=True)
        for cmd in cls._get_all_commands():
            description = cmd.__doc__.strip()
            subparser = subparsers.add_parser(cmd.name, description=description)
            cmd.add_arguments(subparser)

        return parser


def admin_entry_point():
    def callback(arguments, env):
        func = CaerpAdminCommandsRegistry.get_command(arguments.subcommand)
        return func(arguments, env)

    try:
        try:
            # We need to bootstrap the app in order to collect commands registered by
            # plugins. Even required to build the doc.
            ini_file = sys.argv[1]
            pyramid_env = bootstrap(ini_file)
            parser = CaerpAdminCommandsRegistry.get_argument_parser()
            return argparse_command(callback, parser, pyramid_env)
        except IndexError:
            print("No ini file specified, plugin commands won't be listed")
            sys.exit(1)
    finally:
        pass
