"""Create Product Categories

Revision ID: 7623393be1e4
Revises: f050ae45e0ad
Create Date: 2026-08-05 17:53:09.541543

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import TINYINT
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '7623393be1e4'
down_revision: Union[str, Sequence[str], None] = 'f050ae45e0ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('product_categories',
    sa.Column('id', sa.String(36), primary_key=True), 
    sa.Column('organization_id',sa.String(36),sa.ForeignKey('organizations.id',ondelete='CASCADE'),nullable=False), 
    sa.Column('name',sa.String(255),nullable=False),
    sa.Column('description',sa.Text(),nullable=True),
    sa.Column('slug', sa.String(255), nullable=False, unique = True),
    sa.Column('image',sa.String(255),nullable=True),
    sa.Column('is_active', TINYINT(1), nullable=False, server_default=sa.text('1')),
    sa.Column('created_at',sa.DateTime,server_default=sa.text('CURRENT_TIMESTAMP')),
    sa.Column('updated_at',sa.DateTime,server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('product_categories')
