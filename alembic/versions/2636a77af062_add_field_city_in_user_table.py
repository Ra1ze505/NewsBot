"""add field city in user table

Revision ID: 2636a77af062
Revises: 0dd2287b640d
Create Date: 2022-05-23 00:09:20.931718

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2636a77af062'
down_revision = '0dd2287b640d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('city', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'city')
    # ### end Alembic commands ###
