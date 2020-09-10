"""empty message

Revision ID: 68125bdebac6
Revises: 068d6d2b4acd
Create Date: 2020-09-10 16:21:17.949393

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68125bdebac6'
down_revision = '068d6d2b4acd'
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