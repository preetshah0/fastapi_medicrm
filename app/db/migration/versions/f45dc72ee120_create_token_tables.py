"""Create user refresh tokens and personal access tokens tables

Revision ID: f45dc72ee120
Revises: 0e8e910ec0d6
Create Date: 2026-06-26 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f45dc72ee120'
down_revision: Union[str, Sequence[str], None] = '0e8e910ec0d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'user_refresh_tokens',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('token', sa.String(512), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('revoked_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    op.create_index(op.f('ix_user_refresh_tokens_user_id'), 'user_refresh_tokens', ['user_id'], unique=False)
    op.create_index(op.f('ix_user_refresh_tokens_token'), 'user_refresh_tokens', ['token'], unique=True)

    

def downgrade() -> None:
    op.drop_index(op.f('ix_user_refresh_tokens_token'), table_name='user_refresh_tokens')
    op.drop_index(op.f('ix_user_refresh_tokens_user_id'), table_name='user_refresh_tokens')
    op.drop_table('user_refresh_tokens')
