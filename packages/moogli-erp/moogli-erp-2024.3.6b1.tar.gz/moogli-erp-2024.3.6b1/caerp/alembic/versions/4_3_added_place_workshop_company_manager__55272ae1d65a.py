"""4.3 Added place, workshop_company_manager and tags to Workshop

Revision ID: 55272ae1d65a
Revises: 24119bbaeaad
Create Date: 2019-01-24 15:55:00.092513

"""

# revision identifiers, used by Alembic.
revision = "55272ae1d65a"
down_revision = "24119bbaeaad"

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


def update_database_structure():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "workshop", sa.Column("company_manager_id", sa.Integer(), nullable=True)
    )
    op.add_column("workshop", sa.Column("place", sa.Text(), nullable=True))
    op.create_foreign_key(
        op.f("fk_workshop_company_manager_id"),
        "workshop",
        "company",
        ["company_manager_id"],
        ["id"],
    )
    ### end Alembic commands ###


def migrate_datas():
    from caerp_base.models.base import DBSESSION

    session = DBSESSION()
    from alembic.context import get_bind

    conn = get_bind()


def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        op.f("fk_workshop_company_manager_id"), "workshop", type_="foreignkey"
    )
    op.drop_column("workshop", "place")
    op.drop_column("workshop", "company_manager_id")
    ### end Alembic commands ###
