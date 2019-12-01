"""empty message

Revision ID: 94c14de65644
Revises: 0456df43f272
Create Date: 2019-11-30 23:27:10.573384

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94c14de65644'
down_revision = '0456df43f272'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('campaign', sa.Column('creationDate', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('campaign', 'creationDate')
    # ### end Alembic commands ###