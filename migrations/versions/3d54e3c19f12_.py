"""empty message

Revision ID: 3d54e3c19f12
Revises: b402fb459854
Create Date: 2022-07-18 15:49:03.046984

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d54e3c19f12'
down_revision = 'b402fb459854'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sn_election', sa.Column('organization_public_id', sa.String(length=32), nullable=True))
    op.alter_column('sn_election', 'public_id',
               existing_type=sa.VARCHAR(length=32),
               type_=sa.String(length=37),
               existing_nullable=False)
    op.drop_constraint('sn_election_organization_id_fkey', 'sn_election', type_='foreignkey')
    op.create_foreign_key(None, 'sn_election', 'sn_organization', ['organization_public_id'], ['public_id'])
    op.drop_column('sn_election', 'organization_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sn_election', sa.Column('organization_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'sn_election', type_='foreignkey')
    op.create_foreign_key('sn_election_organization_id_fkey', 'sn_election', 'sn_organization', ['organization_id'], ['id'])
    op.alter_column('sn_election', 'public_id',
               existing_type=sa.String(length=37),
               type_=sa.VARCHAR(length=32),
               existing_nullable=False)
    op.drop_column('sn_election', 'organization_public_id')
    # ### end Alembic commands ###
