"""empty message

Revision ID: a824c856db92
Revises: 70e6b91affc9
Create Date: 2020-09-10 15:38:24.185958

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a824c856db92'
down_revision = '70e6b91affc9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'suscripcion', 'group', ['group_id'], ['id'])
    op.create_foreign_key(None, 'suscripcion', 'contact', ['contact_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'suscripcion', type_='foreignkey')
    op.drop_constraint(None, 'suscripcion', type_='foreignkey')
    # ### end Alembic commands ###
