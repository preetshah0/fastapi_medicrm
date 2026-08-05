"""Create Appointments Table

Revision ID: 172d0c0177c1
Revises: d147e53b475b
Create Date: 2026-07-25 22:48:42.959443

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '172d0c0177c1'
down_revision: Union[str, Sequence[str], None] = 'd147e53b475b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "appointments",
        sa.Column('id', sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4())),
        sa.Column('branch_id', sa.String(36), sa.ForeignKey('branches.id', ondelete='CASCADE'), nullable=False),
        sa.Column('doctor_id',sa.String(36),sa.ForeignKey('users.id',ondelete='CASCADE'),nullable=False),
        sa.Column('patient_id', sa.String(36), sa.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False),
        sa.Column('appointment_date', sa.Date(), nullable=True),
        sa.Column('location', sa.String(255),nullable=True),
        sa.Column('start_time',sa.Time(),nullable=True),
        sa.Column('end_time',sa.Time(),nullable=True),
        sa.Column('status',sa.String(255),nullable=False, default="scheduled"),
        sa.Column('type',sa.String(255),nullable=False, default="general_consultation"),
        sa.Column('duration_minutes',sa.Integer(),nullable=False, default=30),
        sa.Column('notes', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('appointments')
