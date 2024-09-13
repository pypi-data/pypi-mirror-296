"""add model_version_id [bf2120261b5a].

Revision ID: bf2120261b5a
Revises: 0.64.0
Create Date: 2024-08-07 11:31:00.661089

"""

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "bf2120261b5a"
down_revision = "0.64.0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade database schema and/or data, creating a new revision."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("pipeline_run", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "model_version_id",
                sqlmodel.sql.sqltypes.GUID(),
                nullable=True,
            )
        )
        batch_op.create_foreign_key(
            "fk_pipeline_run_model_version_id_model_version",
            "model_version",
            ["model_version_id"],
            ["id"],
            ondelete="SET NULL",
        )

    with op.batch_alter_table("step_run", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "model_version_id",
                sqlmodel.sql.sqltypes.GUID(),
                nullable=True,
            )
        )
        batch_op.create_foreign_key(
            "fk_step_run_model_version_id_model_version",
            "model_version",
            ["model_version_id"],
            ["id"],
            ondelete="SET NULL",
        )

    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade database schema and/or data back to the previous revision."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("step_run", schema=None) as batch_op:
        batch_op.drop_constraint(
            "fk_step_run_model_version_id_model_version", type_="foreignkey"
        )
        batch_op.drop_column("model_version_id")

    with op.batch_alter_table("pipeline_run", schema=None) as batch_op:
        batch_op.drop_constraint(
            "fk_pipeline_run_model_version_id_model_version",
            type_="foreignkey",
        )
        batch_op.drop_column("model_version_id")

    # ### end Alembic commands ###
