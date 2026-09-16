"""Create Notes Table

Revision ID: d147e53b475b
Revises: 6f380d73dcc1
Create Date: 2026-07-21 22:57:00.566555

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'd147e53b475b'
down_revision: Union[str, Sequence[str], None] = '6f380d73dcc1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "notes",
        sa.Column('id',sa.String(36),primary_key=True,default=lambda:str(uuid.uuid4())),
        sa.Column('patient_id',sa.String(36),sa.ForeignKey('patients.id',ondelete='CASCADE'),nullable=False),
        sa.Column('user_id',sa.String(36),sa.ForeignKey('users.id',ondelete='CASCADE'),nullable=False),
        sa.Column('notes',sa.Text,nullable=False),
        sa.Column('note_date',sa.Date(),nullable=True),
        sa.Column('written_by',sa.String(255),nullable=True),
        sa.Column('created_at',sa.DateTime,nullable=False,server_default=sa.func.now()),
        sa.Column('updated_at',sa.DateTime,nullable=False,server_default=sa.func.now()),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('notes')
