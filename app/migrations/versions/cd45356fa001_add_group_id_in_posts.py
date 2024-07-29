"""Add group_id in Posts

Revision ID: cd45356fa001
Revises: a702ecdf94b7
Create Date: 2024-07-29 12:04:10.677925

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd45356fa001'
down_revision: Union[str, None] = 'a702ecdf94b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('group_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'posts', 'groups', ['group_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.drop_column('posts', 'group_id')
    # ### end Alembic commands ###
