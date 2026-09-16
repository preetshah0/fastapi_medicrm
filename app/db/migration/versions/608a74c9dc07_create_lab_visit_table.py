"""Create Lab Visit Table

Revision ID: 608a74c9dc07
Revises: eb7c10d0cb30
Create Date: 2026-07-07 20:05:09.218924

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
import uuid


# revision identifiers, used by Alembic.
revision: str = '608a74c9dc07'
down_revision: Union[str, Sequence[str], None] = 'eb7c10d0cb30'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('lab_visits',
        sa.Column('id', sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4())),
        sa.Column('lab_id', sa.String(36), sa.ForeignKey('laboratories.id', ondelete='CASCADE'), nullable=False),
        sa.Column('visited_date', sa.Date(), nullable=True),
        sa.Column('visit_time',sa.Time(),nullable=True),
        sa.Column('name',sa.String(255),nullable=True),
        sa.Column('email',sa.String(255),nullable=True),
        sa.Column('speciality', sa.String(255), nullable=True),
        sa.Column('from_facility',sa.String(255),nullable=True),
        sa.Column('notes', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('lab_visits')
