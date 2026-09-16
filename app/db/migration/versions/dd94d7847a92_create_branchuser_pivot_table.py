"""Create BranchUser Pivot Table

Revision ID: dd94d7847a92
Revises: a14549430b26
Create Date: 2026-06-29 22:22:55.510542

"""
from typing import Sequence, Union
from sqlalchemy import text
from datetime import datetime
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'dd94d7847a92'
down_revision: Union[str, Sequence[str], None] = 'a14549430b26'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('branch_users',
    sa.Column('branch_id', sa.String(36), sa.ForeignKey('branches.id')),
    sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id')),
    sa.Column('role_id', sa.String(36), sa.ForeignKey('roles.id')),
    sa.Column('status', sa.String(255), nullable=False, server_default='active'),
    sa.Column('user_roles', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('branch_id', 'user_id', 'role_id'),
    sa.Column('created_at', sa.DateTime(), nullable=False, server_default=text('CURRENT_TIMESTAMP')),
    sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('branch_users')
