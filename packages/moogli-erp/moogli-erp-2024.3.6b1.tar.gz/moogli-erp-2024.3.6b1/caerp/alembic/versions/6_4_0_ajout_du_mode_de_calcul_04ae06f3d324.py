"""6.4.0 Catalogue : Ajout du mode de calcul

Revision ID: 04ae06f3d324
Revises: 914fba36e9ce
Create Date: 2021-11-30 17:35:50.519552

"""

# revision identifiers, used by Alembic.
revision = "04ae06f3d324"
down_revision = "914fba36e9ce"

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


def update_database_structure():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "base_sale_product", sa.Column("mode", sa.String(length=20), nullable=False)
    )
    op.add_column("base_sale_product", sa.Column("ttc", sa.BigInteger(), nullable=True))
    op.add_column(
        "sale_catalog_work_item",
        sa.Column("_mode", sa.String(length=20), nullable=False),
    )
    op.add_column("company", sa.Column("use_margin_rate_in_catalog", sa.Boolean()))

    table = "sale_catalog_work_item"

    op.drop_constraint(
        "fk_sale_catalog_work_item__product_id", table, type_="foreignkey"
    )
    op.drop_constraint("fk_sale_catalog_work_item__tva_id", table, type_="foreignkey")

    for key in ("_general_overhead", "_margin_rate", "_tva_id", "_product_id"):
        op.drop_column(table, key)
    # ### end Alembic commands ###


def migrate_datas():
    from alembic.context import get_bind
    from zope.sqlalchemy import mark_changed
    from caerp_base.models.base import DBSESSION

    session = DBSESSION()
    session.execute("update company set use_margin_rate_in_catalog=0")
    table = "sale_catalog_work_item"
    session.execute(f"update {table} set _mode='ht';")
    session.execute(
        f"update {table} set _mode='supplier_ht', _ht=0,total_ht=0 where _supplier_ht is not null"
        " and _supplier_ht > 0 and locked = 0;"
    )

    table = "base_sale_product"
    session.execute(f"update {table} set mode='ht';")
    session.execute(
        f"update {table} set mode='supplier_ht', ht=0 where supplier_ht is not null"
        " and supplier_ht > 0;"
    )

    from caerp.models.sale_product.base import BaseSaleProduct
    from caerp.models.sale_product import WorkItem

    """
    NB : On désactive la synchronisation des prix pour la migration en 6.4
    car ça prend un temps énorme et qu'on va revenir sur les calculs rapidement
    en remettant la gestion des coefficients par produit (cf #3389)

    for p in BaseSaleProduct.query():
        p.sync_amounts()

    for wi in WorkItem.query():
        wi.sync_amounts()
    """
    session.execute(
        """update company join (
            select count(id) as cmpt, company_id
            from base_sale_product
            where margin_rate > 0 OR general_overhead > 0
        ) as c on c.company_id=company.id
        set use_margin_rate_in_catalog=1 where c.cmpt > 1
"""
    )
    session.execute(
        """
          update base_sale_product
          set margin_rate= 1 - (1-ifnull(margin_rate,0)) / (1+general_overhead)
          where  general_overhead>0;
          """
    )

    mark_changed(session)
    session.flush()


def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("base_sale_product", "ttc")
    op.drop_column("base_sale_product", "mode")
