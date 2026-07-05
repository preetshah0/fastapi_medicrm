"""Create Supplier Visit Table

Revision ID: f39bfc9a86fd
Revises: 7b8740b7cf57
Create Date: 2026-07-05 19:05:17.455068

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'f39bfc9a86fd'
down_revision: Union[str, Sequence[str], None] = '7b8740b7cf57'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('supplier_visits',
    sa.Column('id', sa.String(36), primary_key=True),   
    sa.Column('supplier_id',sa.String(36),sa.ForeignKey('suppliers.id',ondelete='CASCADE'),nullable=False),
    sa.Column('supplier_name',sa.String(255),nullable=True),
    sa.Column('visited_date',sa.Date,server_default=sa.text('CURRENT_DATE')),
    sa.Column('batch_number',sa.String(255),nullable=True),
    sa.Column('visit_purpose',sa.String(255),nullable=False, server_default = "delivery"),
    sa.Column('notes', sa.String(255), nullable=True),
    sa.Column('created_at',sa.DateTime,server_default=sa.text('CURRENT_TIMESTAMP')),
    sa.Column('updated_at',sa.DateTime,server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
    )
