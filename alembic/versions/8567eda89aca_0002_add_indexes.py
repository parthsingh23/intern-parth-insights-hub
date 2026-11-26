"""0002_add_indexes

Revision ID: 8567eda89aca
Revises: 996daecdfb83
Create Date: 2026-11-26 22:41:55.058170

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8567eda89aca"
down_revision: Union[str, Sequence[str], None] = "996daecdfb83"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "idx_sales_invoice_date",
        "sales",
        ["invoice_date"],
    )
    op.create_index(
        "idx_sales_distributor_id",
        "sales",
        ["distributor_id"],
    )
    op.create_index(
        "idx_sales_sku_id",
        "sales",
        ["sku_id"],
    )


def downgrade() -> None:
    op.drop_index("idx_sales_sku_id", table_name="sales")
    op.drop_index("idx_sales_distributor_id", table_name="sales")
    op.drop_index("idx_sales_invoice_date", table_name="sales")
