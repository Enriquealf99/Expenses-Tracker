"""empty message

Revision ID: 3520afabd4b0
Revises: 7f547c1d6a7b
Create Date: 2024-09-04 13:43:39.492983

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3520afabd4b0'
down_revision = '7f547c1d6a7b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('expense', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'category', ['category_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('expense', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('category_id')

    # ### end Alembic commands ###
