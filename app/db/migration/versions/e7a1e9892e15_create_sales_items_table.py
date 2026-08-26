"""Create Sales Items Table

Revision ID: e7a1e9892e15
Revises: 6252d7af50e2
Create Date: 2026-08-20 10:06:12.178430

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'e7a1e9892e15'
down_revision: Union[str, Sequence[str], None] = '6252d7af50e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "sales_items",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("sale_id", sa.String(36), sa.ForeignKey("sales.id", ondelete="CASCADE"), nullable=False),
        sa.Column("product_id", sa.String(36), sa.ForeignKey("products.id", ondelete="CASCADE"), nullable=False),
        sa.Column("inventory_id", sa.String(36), sa.ForeignKey("inventories.id", ondelete="CASCADE"), nullable=True),
        sa.Column("inventory_batch_id", sa.String(36), sa.ForeignKey("batches.id", ondelete="CASCADE"), nullable=True),
        sa.Column("sale_unit",sa.String(255), nullable=False, server_default="unit"),
        sa.Column("quantity", sa.Integer, nullable=False, server_default="0"),
        sa.Column("base_unit_quantity", sa.Integer, nullable=False, server_default="0"),
        sa.Column("unit_price", sa.Float, nullable=False, server_default="0.00"),
        sa.Column("discount", sa.Float, nullable=False, server_default="0.00"),
        sa.Column("final_amount", sa.Float, nullable=False, server_default="0.00"),
        sa.Column("created_at", sa.DateTime, nullable=True, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=True, server_default=sa.func.now())
    )
    


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('sales_items')
