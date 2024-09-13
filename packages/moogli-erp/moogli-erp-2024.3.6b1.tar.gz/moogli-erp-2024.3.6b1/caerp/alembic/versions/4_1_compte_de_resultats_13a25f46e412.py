"""4.1 : compte de resultats

Revision ID: 13a25f46e412
Revises: 4299e583631c
Create Date: 2018-01-06 12:52:36.054138

"""

# revision identifiers, used by Alembic.
revision = "13a25f46e412"
down_revision = "4299e583631c"

from alembic import op
import sqlalchemy as sa
from caerp.alembic import utils


def update_database_structure():
    utils.add_column(
        "accounting_operation_upload", sa.Column("filetype", sa.String(50))
    )
    utils.add_column("accounting_operation", sa.Column("date", sa.Date()))
    if utils.column_exists("accounting_operation", "datetime"):
        op.drop_column("accounting_operation", "datetime")
    op.alter_column(
        "company",
        "contribution",
        existing_type=sa.Integer,
        type_=sa.Float,
        existing_nullable=True,
    )


def migrate_datas():
    from caerp_base.models.base import DBSESSION

    session = DBSESSION()
    from caerp.models.accounting.operations import AccountingOperationUpload

    for entry in AccountingOperationUpload.query():
        entry.filetype = "analytical_balance"
        session.merge(entry)
        session.flush()


def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    op.drop_column("accounting_operation_upload", "filetype")
