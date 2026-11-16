"""Create Test Required Table

Revision ID: cad5c18c73be
Revises: 2e1c602a4bb0
Create Date: 2026-08-31 11:51:52.236086

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'cad5c18c73be'
down_revision: Union[str, Sequence[str], None] = '2e1c602a4bb0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

import uuid
import datetime


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "test_required",
        sa.Column('id',sa.String(36),primary_key=True,default=uuid.uuid4),
        sa.Column('referral_id',sa.String(36),sa.ForeignKey('patient_lab_referrals.id',ondelete='CASCADE'),nullable=False),
        sa.Column('test_name',sa.String(255),nullable=False),
        sa.Column('test_code',sa.String(255),nullable=False),
        sa.Column('test_description',sa.String(255),nullable=True),
        sa.Column('attachments',sa.String(255),nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("test_required")
