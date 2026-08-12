"""Create Batch Table

Revision ID: b3c0b0c9c3f9
Revises: dcc964ab0d4b
Create Date: 2026-08-10 15:54:46.613504

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'b3c0b0c9c3f9'
down_revision: Union[str, Sequence[str], None] = 'dcc964ab0d4b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
 op.create_table(
        'batches',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('inventory_id', sa.String(36), sa.ForeignKey('inventories.id', ondelete='CASCADE'), nullable=False),
        sa.Column('product_id', sa.String(36), sa.ForeignKey('products.id', ondelete='CASCADE'), nullable=False),
        sa.Column('supplier_id', sa.String(36), sa.ForeignKey('suppliers.id', ondelete='SET NULL'), nullable=True),
        
        sa.Column('batch_no', sa.String(255), nullable=False),
        sa.Column('mfg_date', sa.Date(), nullable=True),
        sa.Column('expiry_date', sa.Date(), nullable=False),
        
        # Quantities
        sa.Column('initial_qty', sa.Integer(), nullable=False),
        sa.Column('current_quantity', sa.Integer(), nullable=False),
        sa.Column('subpack_qty', sa.Integer(), nullable=True),
        sa.Column('base_unit_qty', sa.Integer(), nullable=True),
        
        # Pricing Tiers
        sa.Column('batch_cost_price', sa.Numeric(12, 2), nullable=False),              # Total Purchased Price
        sa.Column('mrp', sa.Numeric(12, 2), nullable=True),             # Printed MRP
        sa.Column('batch_selling_price', sa.Numeric(12, 2), nullable=False),              # Unit Selling Price
        sa.Column('base_unit_sp', sa.Numeric(12, 2), nullable=True),
        sa.Column('subpack_sp', sa.Numeric(12, 2), nullable=True),
        sa.Column('pack_sp', sa.Numeric(12, 2), nullable=True),
        
        # Status Flags
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('batch_status', sa.String(50), nullable=False, server_default=sa.text("'in_stock'")),
        
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        
        sa.UniqueConstraint('inventory_id', 'batch_no', name='unique_inventory_batch_no')
    )
def downgrade() -> None:
    op.drop_table('batches')
