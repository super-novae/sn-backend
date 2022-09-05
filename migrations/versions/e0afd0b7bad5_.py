"""empty message

Revision ID: e0afd0b7bad5
Revises: d11f60ba7a3a
Create Date: 2022-09-05 14:48:30.482142

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0afd0b7bad5'
down_revision = 'd11f60ba7a3a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('sn_election', 'programme',
               existing_type=sa.VARCHAR(length=70),
               type_=sa.String(length=100),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('sn_election', 'programme',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=70),
               existing_nullable=True)
    # ### end Alembic commands ###