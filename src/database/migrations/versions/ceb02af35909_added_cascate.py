"""added cascate

Revision ID: ceb02af35909
Revises: bf689da2a4c8
Create Date: 2023-06-07 20:50:32.080857

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ceb02af35909'
down_revision = 'bf689da2a4c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('username', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=254), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=256), autoincrement=False, nullable=False),
    sa.Column('role_id', sa.VARCHAR(length=32), autoincrement=False, nullable=False),
    sa.Column('id', sa.VARCHAR(length=32), autoincrement=False, nullable=False),
    sa.Column('created_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name='users_role_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    sa.UniqueConstraint('email', name='users_email_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('vehicles',
    sa.Column('manufacturer', sa.VARCHAR(length=254), autoincrement=False, nullable=False),
    sa.Column('model', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    sa.Column('license_plate', sa.VARCHAR(length=7), autoincrement=False, nullable=False),
    sa.Column('consumption', sa.NUMERIC(precision=4, scale=2), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.VARCHAR(length=32), autoincrement=False, nullable=False),
    sa.Column('active', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('id', sa.VARCHAR(length=32), autoincrement=False, nullable=False),
    sa.Column('created_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='vehicles_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='vehicles_pkey'),
    sa.UniqueConstraint('license_plate', name='vehicles_license_plate_key')
    )
    op.create_table('roles',
    sa.Column('name', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    sa.Column('id', sa.VARCHAR(length=32), autoincrement=False, nullable=False),
    sa.Column('created_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='roles_pkey'),
    sa.UniqueConstraint('name', name='roles_name_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('rides',
    sa.Column('distance', sa.NUMERIC(precision=5, scale=2), autoincrement=False, nullable=False),
    sa.Column('gas_price', sa.NUMERIC(precision=5, scale=2), autoincrement=False, nullable=False),
    sa.Column('passenger_id', sa.VARCHAR(length=32), autoincrement=False, nullable=False),
    sa.Column('driver_id', sa.VARCHAR(length=32), autoincrement=False, nullable=False),
    sa.Column('total_value', sa.NUMERIC(precision=5, scale=2), autoincrement=False, nullable=False),
    sa.Column('id', sa.VARCHAR(length=32), autoincrement=False, nullable=False),
    sa.Column('created_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['driver_id'], ['users.id'], name='rides_driver_id_fkey'),
    sa.ForeignKeyConstraint(['passenger_id'], ['users.id'], name='rides_passenger_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='rides_pkey')
    )
    # ### end Alembic commands ###
