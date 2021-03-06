"""empty message

Revision ID: ed0d07534594
Revises: 125e72b88866
Create Date: 2020-05-12 14:00:28.822095

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed0d07534594'
down_revision = '125e72b88866'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('follows_follower_id_key', 'follows', type_='unique')
    op.create_unique_constraint(None, 'posts', ['photo'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'posts', type_='unique')
    op.create_unique_constraint('follows_follower_id_key', 'follows', ['follower_id'])
    # ### end Alembic commands ###
