"""Create Supplier Table

Revision ID: 7b8740b7cf57
Revises: 376678567f44
Create Date: 2026-07-05 18:06:31.079791

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '7b8740b7cf57'
down_revision: Union[str, Sequence[str], None] = '376678567f44'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('suppliers',
    sa.Column('id', sa.String(36), primary_key=True),   
    sa.Column('organization_id', sa.String(36), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False),
    sa.Column('branch_id', sa.String(36), sa.ForeignKey('branches.id', ondelete='CASCADE'), nullable=False),
    sa.Column('type', sa.String(255), nullable=False, server_default="direct_supplier"),
    sa.Column('reps_id',sa.String(36),sa.ForeignKey('medical_representatives.id',ondelete='CASCADE'),nullable=True),
    sa.Column('company',sa.String(255), nullable=True),
    sa.Column('email', sa.String(255), nullable=True),
    sa.Column('phone', sa.String(255), nullable=True),
    sa.Column('notes', sa.String(255), nullable=True),
    sa.Column('created_at',sa.DateTime,server_default=sa.text('CURRENT_TIMESTAMP')),
    sa.Column('updated_at',sa.DateTime,server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('suppliers')
