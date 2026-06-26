"""Create users table

Revision ID: 0e8e910ec0d6
Revises: 
Create Date: 2026-05-10 01:56:11.204806

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '0e8e910ec0d6'
down_revision: Union[str, Sequence[str], None] = '2e5ecd87b057'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
  
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('name', sa.String(50)),
        sa.Column('email', sa.String(255)),
        sa.Column('password',sa.String(255), nullable = False),
        sa.Column('description', sa.Unicode(200)),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('specialization', sa.String(255), nullable=True),
        sa.Column('role', sa.String(50), server_default='staff', nullable=False),
        sa.Column('status', sa.String(255), server_default='active'),
        sa.Column('profile_photo', sa.String(255), nullable=True),
        sa.Column('organization_id', sa.String(36), nullable=True),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='SET NULL'),
        
        # Laravel-style Remember Token
        sa.Column('remember_token', sa.String(100), nullable=True),
        
        # Timestamps
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.Column('deleted_at', sa.DateTime(), nullable=True) # Soft Delete
    
    )

    


def downgrade() -> None:
   op.drop_table('users')
