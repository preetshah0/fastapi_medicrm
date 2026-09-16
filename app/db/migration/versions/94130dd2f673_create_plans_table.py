"""Create Plans Table

Revision ID: 94130dd2f673
Revises: cad5c18c73be
Create Date: 2026-09-11 10:23:01.414455

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import uuid


# revision identifiers, used by Alembic.
revision: str = '94130dd2f673'
down_revision: Union[str, Sequence[str], None] = 'cad5c18c73be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'plans',
        sa.Column('id', sa.String(36), primary_key=True, default=uuid.uuid4),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('slug', sa.String(255), nullable=False, unique=True),
        sa.Column('monthly_price', sa.Numeric(10, 2), nullable=False, server_default='0.00'),
        sa.Column('yearly_price', sa.Numeric(10, 2), nullable=False, server_default='0.00'),
        sa.Column('tagline', sa.Text, nullable=True),
        sa.Column('status', sa.String(50), nullable=False, server_default='draft'),
        sa.Column('modules', sa.JSON, nullable=False, server_default=sa.text("('{}')")),
        sa.Column('max_appointments', sa.Integer, nullable=True),
        sa.Column('max_patients', sa.Integer, nullable=True),
        sa.Column('max_staff', sa.Integer, nullable=True),
        sa.Column('max_lab_referrals', sa.Integer, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('plans')
