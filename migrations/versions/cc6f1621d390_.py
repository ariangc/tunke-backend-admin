"""empty message

Revision ID: cc6f1621d390
Revises: 
Create Date: 2019-11-20 04:34:13.482521

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc6f1621d390'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('share',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dueDate', sa.DateTime(), nullable=True),
    sa.Column('initialBalance', sa.Float(), nullable=True),
    sa.Column('amortization', sa.Float(), nullable=True),
    sa.Column('interest', sa.Float(), nullable=True),
    sa.Column('commission', sa.Float(), nullable=True),
    sa.Column('feeAmount', sa.Float(), nullable=True),
    sa.Column('idLoan', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['idLoan'], ['loan.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('share')
    # ### end Alembic commands ###
