"""empty message

Revision ID: 90ad061e586b
Revises: 
Create Date: 2021-03-31 16:49:06.050426

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90ad061e586b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('something', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'something')
    # ### end Alembic commands ###
