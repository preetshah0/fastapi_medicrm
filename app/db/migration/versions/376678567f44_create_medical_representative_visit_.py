"""Create Medical Representative Visit Table

Revision ID: 376678567f44
Revises: d1f1a0ce4ad8
Create Date: 2026-07-05 13:39:30.054176

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '376678567f44'
down_revision: Union[str, Sequence[str], None] = 'd1f1a0ce4ad8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('mr_visits',
    sa.Column('id',sa.String(36),primary_key=True,default=lambda:str(uuid.uuid4())),
    sa.Column('reps_id',sa.String(36),sa.ForeignKey('medical_representatives.id',ondelete='CASCADE'),nullable=False),
    sa.Column('visited_date',sa.DateTime,nullable=False),
    sa.Column('notes',sa.String(255),nullable=True),
    sa.Column('visit_purpose',sa.String(255),nullable=True),
    sa.Column('Product', sa.String(255),nullable=True),
    sa.Column('created_at',sa.DateTime,server_default=sa.text('CURRENT_TIMESTAMP')),
    sa.Column('updated_at',sa.DateTime,server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
    )
    


def downgrade() -> None:
    """Downgrade schema."""
    pass
