"""empty message

Revision ID: 0c4f2e3132cf
Revises: 3c53f12886ea
Create Date: 2022-02-23 19:39:38.659951

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c4f2e3132cf'
down_revision = '3c53f12886ea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('mod', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'mod')
    # ### end Alembic commands ###
