"""empty message

Revision ID: 6153e3254d01
Revises: b4862d4e28ef
Create Date: 2022-07-27 13:14:44.984536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6153e3254d01'
down_revision = 'b4862d4e28ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sn_voter', sa.Column('college', sa.String(length=100), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sn_voter', 'college')
    # ### end Alembic commands ###