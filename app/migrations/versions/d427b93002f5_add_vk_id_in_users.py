"""Add vk_id in Users

Revision ID: d427b93002f5
Revises: e11487fee7e4
Create Date: 2024-07-26 11:17:02.436492

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd427b93002f5'
down_revision: Union[str, None] = 'e11487fee7e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('vk_id', sa.Integer(), nullable=False))
    op.create_unique_constraint(None, 'users', ['vk_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'vk_id')
    # ### end Alembic commands ###
