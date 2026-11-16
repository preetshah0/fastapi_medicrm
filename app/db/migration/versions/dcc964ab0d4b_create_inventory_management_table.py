"""Create Inventory Management Table

Revision ID: dcc964ab0d4b
Revises: 14fd6f0ddfff
Create Date: 2026-08-10 10:03:59.153003

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'dcc964ab0d4b'
down_revision: Union[str, Sequence[str], None] = '14fd6f0ddfff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'inventories',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('organization_id', sa.String(36), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False),
        sa.Column('branch_id', sa.String(36), sa.ForeignKey('branches.id', ondelete='CASCADE'), nullable=False),
        sa.Column('product_id', sa.String(36), sa.ForeignKey('products.id', ondelete='CASCADE'), nullable=False, unique=True),
        sa.Column('low_stock_threshold', sa.Integer(), nullable=False, server_default=sa.text('10')),
        sa.Column('total_qty', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('inventory_status', sa.String(50), nullable=False, server_default=sa.text("'in_stock'")),
        # sa.Column('total_expired_batches', sa.Integer(), nullable=False, server_default=sa.text('0')),
        
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
    )

def downgrade() -> None:
    op.drop_table('inventories')
