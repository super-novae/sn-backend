"""empty message

Revision ID: 776df943f344
Revises: f970ebe74ebc
Create Date: 2022-07-22 15:07:14.376262

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '776df943f344'
down_revision = 'f970ebe74ebc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sn_candidate', sa.Column('profile_image_url', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sn_candidate', 'profile_image_url')
    # ### end Alembic commands ###
