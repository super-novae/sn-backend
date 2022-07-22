"""empty message

Revision ID: 00adabc86688
Revises: 776df943f344
Create Date: 2022-07-22 15:33:33.294255

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00adabc86688'
down_revision = '776df943f344'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('sn_election', 'public_id',
               existing_type=sa.VARCHAR(length=37),
               type_=sa.String(length=32),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('sn_election', 'public_id',
               existing_type=sa.String(length=32),
               type_=sa.VARCHAR(length=37),
               existing_nullable=False)
    # ### end Alembic commands ###
