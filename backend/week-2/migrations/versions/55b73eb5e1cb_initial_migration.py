"""
Initial migration

Revision ID: 55b73eb5e1cb
Revises: 
Create Date: 2024-12-11 01:45:28.550916

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '55b73eb5e1cb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Drop dependent tables first
    op.drop_table('transaction_items')  # Depends on inventoryitem and transaction
    op.drop_table('transaction')       # Depends on customer and staff
    op.drop_table('inventoryitem')
    op.drop_table('customer')
    op.drop_table('staff')


def downgrade():
    # Recreate the tables in the correct order
    op.create_table('staff',
        sa.Column('s_id', sa.BIGINT(), server_default=sa.text("nextval('staff_s_id_seq'::regclass)"), autoincrement=True, nullable=False),
        sa.Column('s_name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
        sa.Column('s_email', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
        sa.Column('s_is_admin', sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.Column('s_contact', sa.BIGINT(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint('s_id', name='staff_pkey'),
        postgresql_ignore_search_path=False
    )
    op.create_table('customer',
        sa.Column('c_id', sa.BIGINT(), server_default=sa.text("nextval('customer_c_id_seq'::regclass)"), autoincrement=True, nullable=False),
        sa.Column('c_name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
        sa.Column('c_email', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
        sa.Column('c_contact', sa.BIGINT(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint('c_id', name='customer_pkey'),
        postgresql_ignore_search_path=False
    )
    op.create_table('inventoryitem',
        sa.Column('item_sku', sa.BIGINT(), autoincrement=True, nullable=False),
        sa.Column('item_name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
        sa.Column('item_description', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
        sa.Column('item_price', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
        sa.Column('item_qty', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint('item_sku', name='inventoryitem_pkey')
    )
    op.create_table('transaction',
        sa.Column('t_id', sa.BIGINT(), autoincrement=True, nullable=False),
        sa.Column('c_id', sa.BIGINT(), autoincrement=False, nullable=False),
        sa.Column('s_id', sa.BIGINT(), autoincrement=False, nullable=False),
        sa.Column('t_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
        sa.Column('t_amount', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
        sa.Column('t_category', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(['c_id'], ['customer.c_id'], name='transaction_c_id_fkey'),
        sa.ForeignKeyConstraint(['s_id'], ['staff.s_id'], name='transaction_s_id_fkey'),
        sa.PrimaryKeyConstraint('t_id', name='transaction_pkey')
    )
    op.create_table('transaction_items',
        sa.Column('transaction_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('item_sku', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['item_sku'], ['inventoryitem.item_sku'], name='transaction_items_item_sku_fkey'),
        sa.ForeignKeyConstraint(['transaction_id'], ['transaction.t_id'], name='transaction_items_transaction_id_fkey'),
        sa.PrimaryKeyConstraint('transaction_id', 'item_sku', name='transaction_items_pkey')
    )


    # ### end Alembic commands ###
