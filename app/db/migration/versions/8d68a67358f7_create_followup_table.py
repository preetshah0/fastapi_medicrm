"""Create Followup Table

Revision ID: 8d68a67358f7
Revises: dadfae8ffbab
Create Date: 2026-08-17 10:50:52.160990

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '8d68a67358f7'
down_revision: Union[str, Sequence[str], None] = 'dadfae8ffbab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "followups",
        sa.Column('id', sa.String(36), primary_key=True),   
        sa.Column("prescription_id", sa.String(36), sa.ForeignKey('prescriptions.id', ondelete='CASCADE'), nullable=True),
        sa.Column("appointment_id", sa.String(36), sa.ForeignKey('appointments.id', ondelete='CASCADE'), nullable=True),
        sa.Column("branch_id", sa.String(36), sa.ForeignKey('branches.id', ondelete='CASCADE'), nullable=False),
        sa.Column("organization_id", sa.String(36), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False),
        sa.Column("patient_id", sa.String(36), sa.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False),
        sa.Column("doctor_id", sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column("followable_type", sa.String(255), nullable=False),
        sa.Column("followable_id", sa.String(36), nullable=False),
        sa.Column("followup_date", sa.Date(), nullable=True),
        sa.Column("followup_time", sa.Time(), nullable=True),
        sa.Column("followup_duration", sa.Integer(), server_default="30", nullable=False),
        sa.Column("status", sa.String(50), server_default="scheduled", nullable=False),
        sa.Column("contacted_at", sa.DateTime(), nullable=True),
        sa.Column("visited_status", sa.String(50), server_default="pending", nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("followups")
