"""Create Branch Table

Revision ID: a14549430b26
Revises: 0e1bed8d4ba6
Create Date: 2026-06-28 21:32:19.854976

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'a14549430b26'
down_revision: Union[str, Sequence[str], None] = '0e1bed8d4ba6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('Branches', 
        sa.Column('id', sa.String(36), primary_key=True), 
        sa.Column("organization_id", sa.String(36), nullable=False),
        sa.Column("branch_name", sa.String(255), nullable=False),
        sa.Column("branch_email", sa.String(255), nullable=False),
        sa.Column("phone_number", sa.String(20), nullable=True),
        sa.Column("status", sa.String(255), nullable=False, server_default='active'),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("city", sa.String(255), nullable=True),
        sa.Column("state", sa.String(255), nullable=True),
        sa.Column("opening_time", sa.Time(), nullable=True),
        sa.Column("closing_time", sa.Time(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('Branches')
    
