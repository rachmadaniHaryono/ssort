"""Example revision

Revision ID: fdf0cf6487a3
Revises:
Create Date: 2021-08-09 17:55:19.491713

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fdf0cf6487a3"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "example",
        sa.Column("example_id", sa.Integer(), nullable=False),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("measurements")
    # ### end Alembic commands ###
