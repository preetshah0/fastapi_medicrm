"""Create Prescription Medication Table

Revision ID: dadfae8ffbab
Revises: 0649d0280cad
Create Date: 2026-08-12 12:17:55.058052

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'dadfae8ffbab'
down_revision: Union[str, Sequence[str], None] = '0649d0280cad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'prescription_medications',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('prescription_id', sa.String(36), sa.ForeignKey('prescriptions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('inventory_id', sa.String(36), sa.ForeignKey('inventories.id', ondelete='SET NULL'), nullable=True),
        sa.Column('inventory_batch_id', sa.String(36), sa.ForeignKey('batches.id', ondelete='SET NULL'), nullable=True),
        sa.Column('drug_name', sa.String(255), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('dosage', sa.String(255), nullable=True),
        sa.Column('frequency', sa.String(255), nullable=True),
        sa.Column('meal_timing', sa.String(255), nullable=True),
        sa.Column('duration', sa.String(255), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.func.now())
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('prescription_medications')
