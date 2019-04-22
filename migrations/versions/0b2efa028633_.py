"""empty message

Revision ID: 0b2efa028633
Revises: 159371b77a4d
Create Date: 2019-04-04 14:35:14.122151

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b2efa028633'
down_revision = '159371b77a4d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('candidates_status', sa.Column('admission_date', sa.Date(), nullable=True))
    op.add_column('revoked_tokens', sa.Column('expires', sa.Date(), nullable=True))
    op.add_column('revoked_tokens', sa.Column('revoked', sa.Boolean(), nullable=True))
    op.add_column('revoked_tokens', sa.Column('token_type', sa.Text(), nullable=True))
    op.add_column('revoked_tokens', sa.Column('user_id', sa.BigInteger(), nullable=True))
    op.drop_column('revoked_tokens', 'expired')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('revoked_tokens', sa.Column('expired', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('revoked_tokens', 'user_id')
    op.drop_column('revoked_tokens', 'token_type')
    op.drop_column('revoked_tokens', 'revoked')
    op.drop_column('revoked_tokens', 'expires')
    op.drop_column('candidates_status', 'admission_date')
    # ### end Alembic commands ###