"""0003_create_sales_denorm_view

Revision ID: e5ac5dff1140
Revises: 8567eda89aca
Create Date: 2026-11-26 22:53:37.288070

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e5ac5dff1140"
down_revision: Union[str, Sequence[str], None] = "8567eda89aca"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE VIEW v_sales_denorm AS
        SELECT
            s.invoice_no AS "Invoice No",
            s.invoice_date AS "Invoice Date",
            r.region_name AS "Region",
            st.state_name AS "State",
            d.distributor_code AS "Dist Code",
            d.distributor_name AS "Distributor Name",
            sku.sku_code AS "SKU Code",
            sku.sku_name AS "SKU Name",
            b.brand_name AS "Brand",
            s.channel AS "Channel",
            s.quantity AS "Qty",
            s.net_value AS "Net Value (INR)",
            s.is_return AS is_return
        FROM sales AS s
        JOIN distributors AS d
            ON s.distributor_id = d.distributor_id
        JOIN states AS st
            ON d.state_id = st.state_id
        JOIN regions AS r
            ON st.region_id = r.region_id
        JOIN skus AS sku
            ON s.sku_id = sku.sku_id
        JOIN brands AS b
            ON sku.brand_id = b.brand_id;
    """)


def downgrade() -> None:
    op.execute("DROP VIEW IF EXISTS v_sales_denorm;")
