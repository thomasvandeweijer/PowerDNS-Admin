"""Init DB

Revision ID: 787bdba9e147
Revises: 
Create Date: 2018-06-22 09:45:58.941559

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '787bdba9e147'
down_revision = None
branch_labels = None
depends_on = None


def seed_data():
    role_table = sa.sql.table('role',
        sa.sql.column('id', sa.Integer),
        sa.sql.column('name', sa.String),
        sa.sql.column('description', sa.String)
    )

    setting_table = sa.sql.table('setting',
        sa.sql.column('id', sa.Integer),
        sa.sql.column('name', sa.String),
        sa.sql.column('value', sa.String)
    )

    template_table = sa.sql.table('domain_template',
        sa.sql.column('id', sa.Integer),
        sa.sql.column('name', sa.String),
        sa.sql.column('description', sa.String)
    )

    op.bulk_insert(role_table,
        [
            {'id': 1, 'name': 'Administrator', 'description': 'Administrator'},
            {'id': 2, 'name': 'User', 'description': 'User'}
        ]
    )

    op.bulk_insert(setting_table,
        [
            {'id': 1, 'name': 'maintenance', 'value': 'False'},
            {'id': 2, 'name': 'fullscreen_layout', 'value': 'True'},
            {'id': 3, 'name': 'record_helper', 'value': 'True'},
            {'id': 4, 'name': 'login_ldap_first', 'value': 'True'},
            {'id': 5, 'name': 'default_record_table_size', 'value': '15'},
            {'id': 6, 'name': 'default_domain_table_size', 'value': '10'},
            {'id': 7, 'name': 'auto_ptr', 'value': 'False'}
        ]
    )

    op.bulk_insert(template_table,
        [
            {id: 1, 'name': 'basic_template_1', 'description': 'Basic Template #1'},
            {id: 2, 'name': 'basic_template_2', 'description': 'Basic Template #2'},
            {id: 3, 'name': 'basic_template_3', 'description': 'Basic Template #3'}
        ]
    )


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=False),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.Column('contact', sa.String(length=128), nullable=True),
    sa.Column('mail', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_account_name'), 'account', ['name'], unique=True)
    op.create_table('domain_template',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_domain_template_name'), 'domain_template', ['name'], unique=True)
    op.create_table('history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('msg', sa.String(length=256), nullable=True),
    sa.Column('detail', sa.Text(), nullable=True),
    sa.Column('created_by', sa.String(length=128), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_role_name'), 'role', ['name'], unique=True)
    op.create_table('setting',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('value', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('domain',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('master', sa.String(length=128), nullable=True),
    sa.Column('type', sa.String(length=6), nullable=False),
    sa.Column('serial', sa.Integer(), nullable=True),
    sa.Column('notified_serial', sa.Integer(), nullable=True),
    sa.Column('last_check', sa.Integer(), nullable=True),
    sa.Column('dnssec', sa.Integer(), nullable=True),
    sa.Column('account_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_domain_name'), 'domain', ['name'], unique=True)
    op.create_table('domain_template_record',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('type', sa.String(length=64), nullable=True),
    sa.Column('ttl', sa.Integer(), nullable=True),
    sa.Column('data', sa.Text(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('template_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['template_id'], ['domain_template.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password', sa.String(length=64), nullable=True),
    sa.Column('firstname', sa.String(length=64), nullable=True),
    sa.Column('lastname', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=128), nullable=True),
    sa.Column('avatar', sa.String(length=128), nullable=True),
    sa.Column('otp_secret', sa.String(length=16), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('account_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('domain_setting',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('domain_id', sa.Integer(), nullable=True),
    sa.Column('setting', sa.String(length=255), nullable=False),
    sa.Column('value', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['domain_id'], ['domain.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('domain_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('domain_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['domain_id'], ['domain.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###

    # Insert default values to the database
    seed_data()


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('domain_user')
    op.drop_table('domain_setting')
    op.drop_table('account_user')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_table('user')
    op.drop_table('domain_template_record')
    op.drop_index(op.f('ix_domain_name'), table_name='domain')
    op.drop_table('domain')
    op.drop_table('setting')
    op.drop_index(op.f('ix_role_name'), table_name='role')
    op.drop_table('role')
    op.drop_table('history')
    op.drop_index(op.f('ix_domain_template_name'), table_name='domain_template')
    op.drop_table('domain_template')
    op.drop_index(op.f('ix_account_name'), table_name='account')
    op.drop_table('account')
    # ### end Alembic commands ###