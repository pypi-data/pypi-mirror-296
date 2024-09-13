"""6.5.0 champ_requis_task

Revision ID: 115a580ee4a9
Revises: aa5d02b3513f
Create Date: 2022-11-28 16:37:54.032824

"""

# revision identifiers, used by Alembic.
revision = "115a580ee4a9"
down_revision = "aa5d02b3513f"

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from caerp.alembic import utils


def update_database_structure():
    utils.disable_constraints()
    op.alter_column(
        "task",
        "company_id",
        existing_type=mysql.INTEGER(display_width=11),
        nullable=False,
    )
    op.alter_column(
        "task",
        "customer_id",
        existing_type=mysql.INTEGER(display_width=11),
        nullable=False,
    )
    op.alter_column(
        "task",
        "business_type_id",
        existing_type=mysql.INTEGER(display_width=11),
        nullable=False,
    )
    utils.enable_constraints()
    # ### end Alembic commands ###


def migrate_datas():
    from alembic.context import get_bind
    from zope.sqlalchemy import mark_changed
    from caerp_base.models.base import DBSESSION

    session = DBSESSION()
    conn = get_bind()

    mark_changed(session)
    session.flush()


def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    utils.drop_constraints()
    op.alter_column(
        "task",
        "customer_id",
        existing_type=mysql.INTEGER(display_width=11),
        nullable=True,
    )
    op.alter_column(
        "task",
        "company_id",
        existing_type=mysql.INTEGER(display_width=11),
        nullable=True,
    )
    op.alter_column(
        "task",
        "business_type_id",
        existing_type=mysql.INTEGER(display_width=11),
        nullable=True,
    )
    utils.enable_constraints()
    # ### end Alembic commands ###
