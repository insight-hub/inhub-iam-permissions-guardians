"""Profiles: autogenerated

Revision ID: 457edfdfafa8
Revises: 3fbfd7f90976
Create Date: 2023-03-28 08:57:47.735814

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '457edfdfafa8'
down_revision = '3fbfd7f90976'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profiles',
                    sa.Column('uuid', sa.UUID(), nullable=False),
                    sa.Column('name', sa.String(length=30), nullable=True),
                    sa.Column('company_name', sa.String(
                        length=30), nullable=True),
                    sa.Column('bio', sa.String(), nullable=True),
                    sa.Column('location', sa.String(length=30), nullable=True),
                    sa.Column('prefere_language', sa.String(), nullable=True),
                    sa.Column('created_at', sa.DateTime(timezone=True),
                              server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(
                        timezone=True), nullable=True),
                    sa.Column('username', sa.String(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['username'], ['users.username'], ),
                    sa.PrimaryKeyConstraint('uuid')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('profiles')
    # ### end Alembic commands ###