"""kartik

Revision ID: 872c2dbcbc74
Revises: a27ebe7dc58f
Create Date: 2024-05-11 11:22:41.360357

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '872c2dbcbc74'
down_revision = 'a27ebe7dc58f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('body',
               existing_type=sa.VARCHAR(length=140),
               type_=sa.String(length=4000),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('body',
               existing_type=sa.String(length=4000),
               type_=sa.VARCHAR(length=140),
               existing_nullable=False)

    # ### end Alembic commands ###
