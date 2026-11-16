"""Create Report Table

Revision ID: 6f380d73dcc1
Revises: 727f27946e50
Create Date: 2026-07-21 22:50:22.949520

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '6f380d73dcc1'
down_revision: Union[str, Sequence[str], None] = '727f27946e50'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'reports',
        sa.Column('id',sa.String(36),primary_key=True,default=lambda:str(uuid.uuid4())),
        sa.Column('patient_id',sa.String(36),sa.ForeignKey('patients.id',ondelete='CASCADE'),nullable=False),
        sa.Column('report_type',sa.String(255),nullable=False),
        sa.Column('attachment',sa.String(255),nullable=True),
        sa.Column('notes',sa.String(255),nullable=True),
        sa.Column('report_date',sa.Date(),nullable=True),
        sa.Column('created_at',sa.DateTime,nullable=False,server_default=sa.func.now()),
        sa.Column('updated_at',sa.DateTime,nullable=False,server_default=sa.func.now()),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('reports')
