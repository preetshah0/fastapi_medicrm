"""Create Patient Lab Referrals Table

Revision ID: 2e1c602a4bb0
Revises: e7a1e9892e15
Create Date: 2026-08-26 18:15:00.654463

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
import uuid
import datetime


# revision identifiers, used by Alembic.
revision: str = '2e1c602a4bb0'
down_revision: Union[str, Sequence[str], None] = 'e7a1e9892e15'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "patient_lab_referrals",
        sa.Column('id',sa.String(36),primary_key=True,default=uuid.uuid4),
        sa.Column('organization_id', sa.String(36), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False),
        sa.Column('branch_id', sa.String(36), sa.ForeignKey('branches.id', ondelete='CASCADE'), nullable=False),
        sa.Column('doctor_id', sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('patient_id',sa.String(36),sa.ForeignKey('patients.id',ondelete='CASCADE'),nullable=False),
        sa.Column('ref_no',sa.String(255),nullable=False),
        sa.Column('referred_by',sa.String(255),nullable=False),
        sa.Column('clinical_notes',sa.String(255),nullable=True),
        sa.Column('report_id', sa.String(36), sa.ForeignKey('reports.id', ondelete='SET NULL'), nullable=True),
        sa.Column('special_instructions',sa.String(255),nullable=True),
        sa.Column('lab_id',sa.String(36),sa.ForeignKey('laboratories.id',ondelete='CASCADE'),nullable=False),
        sa.Column('priority',sa.String(255),nullable=False,default="low"),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("patient_lab_referrals")
