"""Create permission table

Revision ID: de1fed1ae57f
Revises: 7ae4e2d62d55
Create Date: 2026-06-27 13:36:22.974853

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'de1fed1ae57f'
down_revision: Union[str, Sequence[str], None] = '7ae4e2d62d55'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('permissions', 
    sa.Column('id', sa.String(36), primary_key=True), 
    sa.Column('permission', sa.String(255), nullable=False), 
    sa.Column('slug', sa.String(255), nullable=False, unique = True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')), 
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')), 
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('permissions')