"""empty message

Revision ID: 5762030b8120
Revises: ebdc63a49615
Create Date: 2022-07-05 16:20:11.087521

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5762030b8120'
down_revision = 'ebdc63a49615'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('edi_data_form_id_fkey', 'edi_data', type_='foreignkey')
    op.drop_column('edi_data', 'form_id')
    op.drop_constraint('edi_extra_data_form_id_fkey', 'edi_extra_data', type_='foreignkey')
    op.drop_column('edi_extra_data', 'form_id')
    op.drop_table('form_field')
    op.drop_index('ix_form_name', table_name='form')
    op.drop_table('form')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('form',
                    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('form_id_seq'::regclass)"),
                              autoincrement=True, nullable=False),
                    sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('id', name='form_pkey'),
                    postgresql_ignore_search_path=False
                    )
    op.create_index('ix_form_name', 'form', ['name'], unique=False)
    op.create_table('form_field',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
                    sa.Column('order', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('field_json', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
                    sa.Column('form_id', sa.INTEGER(), autoincrement=False, nullable=False),
                    sa.ForeignKeyConstraint(['form_id'], ['form.id'], name='form_field_form_id_fkey'),
                    sa.PrimaryKeyConstraint('id', name='form_field_pkey')
                    )
    op.add_column('edi_extra_data', sa.Column('form_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('edi_extra_data_form_id_fkey', 'edi_extra_data', 'form', ['form_id'], ['id'])
    op.add_column('edi_data', sa.Column('form_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('edi_data_form_id_fkey', 'edi_data', 'form', ['form_id'], ['id'])
    # ### end Alembic commands ###
