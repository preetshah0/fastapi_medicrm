"""Create Sales Table


Revision ID: 6252d7af50e2
Revises: 8d68a67358f7
Create Date: 2026-08-20 10:05:48.476374

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '6252d7af50e2'
down_revision: Union[str, Sequence[str], None] = '8d68a67358f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('sales',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('organization_id', sa.String(36), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False),
        sa.Column('branch_id', sa.String(36), sa.ForeignKey('branches.id', ondelete='CASCADE'), nullable=False),
        sa.Column('patient_id', sa.String(36), sa.ForeignKey('patients.id', ondelete='CASCADE'), nullable=True),
        sa.Column('prescription_id', sa.String(36), sa.ForeignKey('prescriptions.id', ondelete='CASCADE'), nullable=True),
        sa.Column('invoice_number', sa.String(255), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('phone', sa.String(255), nullable=True),
        sa.Column('total_amount', sa.Float(), nullable=False, server_default='0.00'),
        sa.Column('discount_amount', sa.Float(), nullable=False, server_default='0.00'),
        sa.Column('sub_total', sa.Float(), nullable=False, server_default='0.00'),
        sa.Column('tax_amount', sa.Float(), nullable=False, server_default='0.00'),
        sa.Column('payment_status', sa.String(50), nullable=False, server_default='pending'),
        sa.Column('payment_method', sa.String(50), nullable=False, server_default='cash'),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('sales_status', sa.String(50), nullable=False, server_default='pending'),
        sa.Column('sales_type', sa.String(50), nullable=False, server_default='internal'),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.func.now())
    )


def downgrade() -> None:
    op.drop_table('sales')
