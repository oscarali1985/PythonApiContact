"""empty message

Revision ID: 5167bd9a6d80
Revises: 68125bdebac6
Create Date: 2020-09-10 16:22:34.029301

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5167bd9a6d80'
down_revision = '68125bdebac6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'suscripcion', 'contact', ['contact_id'], ['id'])
    op.create_foreign_key(None, 'suscripcion', 'group', ['group_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'suscripcion', type_='foreignkey')
    op.drop_constraint(None, 'suscripcion', type_='foreignkey')
    # ### end Alembic commands ###