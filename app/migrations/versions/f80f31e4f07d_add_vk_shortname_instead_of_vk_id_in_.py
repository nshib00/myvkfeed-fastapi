"""Add vk_shortname instead of vk_id in Users

Revision ID: f80f31e4f07d
Revises: d427b93002f5
Create Date: 2024-07-27 12:21:25.241487

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f80f31e4f07d'
down_revision: Union[str, None] = 'd427b93002f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('vk_shortname', sa.String(), nullable=False))
    op.drop_constraint('users_vk_id_key', 'users', type_='unique')
    op.create_unique_constraint(None, 'users', ['vk_shortname'])
    op.drop_column('users', 'vk_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('vk_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'users', type_='unique')
    op.create_unique_constraint('users_vk_id_key', 'users', ['vk_id'])
    op.drop_column('users', 'vk_shortname')
    # ### end Alembic commands ###
