"""Add user_id to Expense

Revision ID: 7f547c1d6a7b
Revises: 3fac08daf45a
Create Date: 2024-09-04 13:30:02.595625

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f547c1d6a7b'
down_revision = '3fac08daf45a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('expense', schema=None) as batch_op:
        batch_op.drop_constraint('expense_category_id_fkey', type_='foreignkey')
        batch_op.drop_column('category_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('expense', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('expense_category_id_fkey', 'category', ['category_id'], ['id'])

    # ### end Alembic commands ###