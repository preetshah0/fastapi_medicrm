"""Create Patient Visit Table

Revision ID: f050ae45e0ad
Revises: 00810613de83
Create Date: 2026-07-21 22:43:13.333895

"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'f050ae45e0ad'
down_revision: Union[str, Sequence[str], None] = '00810613de83'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "patient_visits",
        sa.Column('id', sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4())),
        sa.Column('appointment_id', sa.String(36), sa.ForeignKey('appointments.id', ondelete='CASCADE'), nullable=False),
        sa.Column('patient_id', sa.String(36), sa.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False),
        sa.Column('visited_date', sa.Date(), nullable=True),
        sa.Column('visit_time', sa.Time(), nullable=True),
        sa.Column('amount_charged', sa.Float(), nullable=True),
        sa.Column('payment_mode', sa.String(255), nullable=True),
        sa.Column('payment_status', sa.String(255), nullable=True),
        sa.Column('notes', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('patient_visits')
