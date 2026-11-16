"""Create pivot table user_roles

Revision ID: 3425a2fd2779
Revises: de1fed1ae57f
Create Date: 2026-06-27 13:38:28.151779

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '3425a2fd2779'
down_revision: Union[str, Sequence[str], None] = 'de1fed1ae57f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('user_roles', 
    sa.Column('id', sa.String(36), primary_key=True), 
    sa.Column('user_id', sa.String(36), nullable=False), 
    sa.Column('role_id', sa.String(36), nullable=False), 
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')), 
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')), 
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_user_roles_user_id_users')), 
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name=op.f('fk_user_roles_role_id_roles'))) 


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('user_roles')
