"""Create pivot table roles_permissions

Revision ID: 0e1bed8d4ba6
Revises: 3425a2fd2779
Create Date: 2026-06-27 13:39:37.605438

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '0e1bed8d4ba6'
down_revision: Union[str, Sequence[str], None] = '3425a2fd2779'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('roles_permissions', 
    sa.Column('id', sa.String(36), primary_key=True), 
    sa.Column('role_id', sa.String(36), nullable=False), 
    sa.Column('permission_id', sa.String(36), nullable=False), 
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')), 
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')), 
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name=op.f('fk_roles_permissions_role_id_roles')), 
    sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], name=op.f('fk_roles_permissions_permission_id_permissions')))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('roles_permissions')

