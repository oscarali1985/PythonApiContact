"""empty message

Revision ID: 945290b1efa4
Revises: d0c214572f97
Create Date: 2020-09-13 14:46:04.286157

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '945290b1efa4'
down_revision = 'd0c214572f97'
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