"""scores

Revision ID: 557385324afc
Revises: 36df4070eed0
Create Date: 2024-05-16 20:53:35.876758

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '557385324afc'
down_revision: Union[str, None] = '36df4070eed0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('scores', sa.INTEGER(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'scores')
    # ### end Alembic commands ###
