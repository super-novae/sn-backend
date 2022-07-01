"""empty message

Revision ID: 2e7ffb5e8c6a
Revises: 2a3ea18dc4fa
Create Date: 2022-07-01 00:39:32.795006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e7ffb5e8c6a'
down_revision = '2a3ea18dc4fa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('organization',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('public_id', sa.String(length=32), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('public_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('organization')
    # ### end Alembic commands ###
