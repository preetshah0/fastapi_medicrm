"""Create Patient Appointments Table

Revision ID: 00810613de83
Revises: 172d0c0177c1
Create Date: 2026-07-25 23:11:29.596275

"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '00810613de83'
down_revision: Union[str, Sequence[str], None] = '172d0c0177c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "patient_appointments",
        sa.Column('id', sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4())),
        sa.Column('appointment_id', sa.String(36), sa.ForeignKey('appointments.id', ondelete='CASCADE'), nullable=False),
        sa.Column('patient_id', sa.String(36), sa.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False),
        sa.Column('location', sa.String(255), nullable=False),
        sa.Column('appointment_date', sa.Date(), nullable=True),
        sa.Column('appointment_time', sa.Time(), nullable=True),
        sa.Column('duration_minutes', sa.Integer(), nullable=False, default=30),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('patient_appointments')
