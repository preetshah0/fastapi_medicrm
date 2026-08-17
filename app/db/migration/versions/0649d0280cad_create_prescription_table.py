"""Create Prescription Table

Revision ID: 0649d0280cad
Revises: b3c0b0c9c3f9
Create Date: 2026-08-12 11:45:29.489781

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '0649d0280cad'
down_revision: Union[str, Sequence[str], None] = 'b3c0b0c9c3f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'prescriptions',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('branch_id', sa.String(36), sa.ForeignKey('branches.id', ondelete='CASCADE'), nullable=False),
        sa.Column('patient_id', sa.String(36), sa.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False),
        sa.Column('doctor_id', sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('ref_code', sa.String(8), nullable=False),
        sa.Column('diagnosis', sa.Text(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('status', sa.String(50), nullable=False, server_default='draft'),
        # sa.Column('pharmacy_status', sa.String(50), nullable=False, server_default='pending'),
        # sa.Column('amount_to_pay', sa.Numeric(10, 2), nullable=False, server_default='0.00'),
        # sa.Column('payment_method', sa.String(50), nullable=True),
        # sa.Column('payment_status', sa.String(50), nullable=False, server_default='pending'),
        sa.Column('follow_up', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('follow_up_date', sa.Date(), nullable=True),
        sa.Column('follow_up_time', sa.Time(), nullable=True),
        sa.Column('follow_up_note', sa.String(255), nullable=True),
        sa.Column('followup_duration', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.func.now())
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('prescriptions')
