"""Create Subscription Table

Revision ID: 45a899c24433
Revises: 94130dd2f673
Create Date: 2026-09-11 12:55:40.188108

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic.
revision: str = '45a899c24433'
down_revision: Union[str, Sequence[str], None] = '94130dd2f673'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'subscriptions',
        sa.Column('id', sa.String(36), primary_key=True, default=uuid.uuid4),
        sa.Column('plan_id', sa.String(36), sa.ForeignKey('plans.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('organization_id', sa.String(36), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False),
        sa.Column('start_date', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('end_date', sa.DateTime(), nullable=True),
        sa.Column('total_billing_amount', sa.Numeric(10, 2), nullable=False, server_default='0.00'),
        sa.Column('currency', sa.String(50), nullable=False, server_default='INR'),
        sa.Column('billing_period', sa.String(20), nullable=False, server_default='monthly'),
        sa.Column('auto_renew', sa.String(20), nullable=False, server_default='active'),
        sa.Column('cancelled_at', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(50), nullable=False, server_default='active'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
    )
def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('subscriptions')
