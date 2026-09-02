"""create organization table

Revision ID: 2e5ecd87b057
Revises: 0e8e910ec0d6
Create Date: 2026-06-06 06:50:40.348598

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '2e5ecd87b057'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'organizations',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('organization_name', sa.String(255), nullable=False),
        sa.Column('organization_email', sa.String(255), nullable=False),
        sa.Column('ref', sa.String(255), nullable=False),
        # sa.Column('organization_password', sa.String(255), nullable=False, server_default='password'),
        # sa.Column('annual_discount', sa.Float(), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        # sa.Column('plan_type', sa.String(50), nullable=False, server_default='monthly'),
        sa.Column('status', sa.String(255), server_default='active'),
        # sa.Column('plan_id', sa.String(36), nullable=True),
        # sa.ForeignKeyConstraint(['plan_id'], ['plan.id'], ondelete='SET NULL'),
        sa.Column('profile_photo', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.Column('deleted_at', sa.DateTime(), nullable=True)
    )

    
def downgrade() -> None:
    op.drop_table('organizations')  



 