"""Create Laboratory Table

Revision ID: eb7c10d0cb30
Revises: f39bfc9a86fd
Create Date: 2026-07-07 19:37:13.415061

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
import uuid

# revision identifiers, used by Alembic.
revision: str = 'eb7c10d0cb30'
down_revision: Union[str, Sequence[str], None] = 'f39bfc9a86fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('laboratories',
        sa.Column('id',sa.String(36),primary_key=True,default=uuid.uuid4),
        sa.Column('organization_id', sa.String(36), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False),
        sa.Column('branch_id', sa.String(36), sa.ForeignKey('branches.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name',sa.String(255),nullable=True),
        sa.Column('contact_person',sa.String(255),nullable=True),
        sa.Column('facility_type',sa.String(255),nullable=False,server_default='internal'),
        sa.Column('lab_type',sa.String(255),nullable=True),
        sa.Column('lab_type_id',sa.String(36),sa.ForeignKey('master_options.id', ondelete='SET NULL'),nullable=False),
        sa.Column('address',sa.String(255),nullable=True),
        sa.Column('city',sa.String(255),nullable=True),
        sa.Column('pincode',sa.String(255),nullable=True),
        sa.Column('phone_number',sa.String(255),nullable=True),
        sa.Column('email',sa.String(255),nullable=True),
        sa.Column('notes',sa.String(255),nullable=True),
        sa.Column('status',sa.String(255),nullable=False,server_default='active'),
        sa.Column('created_at',sa.DateTime(),nullable=False,server_default=sa.func.now()),
        sa.Column('updated_at',sa.DateTime(),nullable=False,server_default=sa.func.now())
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('laboratories')
