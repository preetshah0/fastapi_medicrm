"""Create Product Table

Revision ID: 14fd6f0ddfff
Revises: 45eaf6df2239
Create Date: 2026-08-07 11:58:21.285927

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '14fd6f0ddfff'
down_revision: Union[str, Sequence[str], None] = '45eaf6df2239'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'products',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('organization_id', sa.String(36), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False),
        sa.Column('branch_id', sa.String(36), sa.ForeignKey('branches.id', ondelete='CASCADE'), nullable=False),
        sa.Column('category_id', sa.String(36), sa.ForeignKey('product_categories.id', ondelete='SET NULL'), nullable=False),
        sa.Column('product_form_id', sa.String(36), sa.ForeignKey('master_options.id', ondelete='SET NULL'), nullable=True),
        sa.Column('size_id', sa.String(36), sa.ForeignKey('master_options.id', ondelete='SET NULL'), nullable=True),
        sa.Column('outer_size_id', sa.String(36), sa.ForeignKey('master_options.id', ondelete='SET NULL'), nullable=True),
        sa.Column('base_unit_id', sa.String(36), sa.ForeignKey('master_options.id', ondelete='SET NULL'), nullable=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('variant', sa.String(255), nullable=True),
        sa.Column('sku', sa.String(255), nullable=False, unique=True, index=True),
        sa.Column('slug', sa.String(255), nullable=False, unique=True, index=True),
        sa.Column('manufacturer', sa.String(255), nullable=True),
        sa.Column('image', sa.String(255), nullable=True),
        sa.Column('dosage_strength', sa.String(255), nullable=True),
        sa.Column('conversion_factor', sa.Integer(), nullable=True),
        sa.Column('packs_per_outer', sa.Integer(), nullable=True),
        sa.Column('low_stock_threshold', sa.Integer(), nullable=False, server_default=sa.text('1')),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_available', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('products')
