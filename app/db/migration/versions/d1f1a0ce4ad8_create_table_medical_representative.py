"""Create Table Medical Representative 

Revision ID: d1f1a0ce4ad8
Revises: dd94d7847a92
Create Date: 2026-07-05 08:17:14.026446

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'd1f1a0ce4ad8'
down_revision: Union[str, Sequence[str], None] = 'dd94d7847a92'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'medical_representatives',
        sa.Column('id', sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4())),
        sa.Column('organization_id', sa.String(36), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False),
        sa.Column('branch_id', sa.String(36), sa.ForeignKey('branches.id', ondelete='CASCADE'), nullable=False),
        sa.Column('reps_name',sa.String(255),nullable=True),
        sa.Column('reps_email',sa.String(255),nullable=True),
        sa.Column('reps_phone',sa.String(255),nullable=True),
        sa.Column('notes',sa.String(255),nullable=True),
        sa.Column('reps_profile_photo',sa.String(255),nullable=True),
        sa.Column('company_name',sa.String(255),nullable=True),
        sa.Column('city',sa.String(255),nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('medical_representatives')
