import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "b6b1ecfc9524"
down_revision = "637920a840f7"
branch_labels = None
depends_on = None


def upgrade(engine_name):
    if engine_name != "flask_state_sqlite":
        return
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    if engine_name != "flask_state_sqlite":
        return
    globals()["downgrade_%s" % engine_name]()


def upgrade_flask_state_sqlite():
    op.add_column(
        "flask_state_io",
        sa.Column(
            "packets_recv",
            mysql.BIGINT(unsigned=True),
            nullable=True,
            server_default=sa.text("0"),
        ),
    )
    op.add_column(
        "flask_state_io",
        sa.Column(
            "packets_sent",
            mysql.BIGINT(unsigned=True),
            nullable=True,
            server_default=sa.text("0"),
        ),
    )
    op.add_column(
        "flask_state_io",
        sa.Column(
            "read_count",
            mysql.BIGINT(unsigned=True),
            nullable=True,
            server_default=sa.text("0"),
        ),
    )
    op.add_column(
        "flask_state_io",
        sa.Column(
            "write_count",
            mysql.BIGINT(unsigned=True),
            nullable=True,
            server_default=sa.text("0"),
        ),
    )


def downgrade_flask_state_sqlite():
    op.create_table(
        "flask_state_io_dg_tmp",
        sa.Column(
            "id",
            mysql.INTEGER(unsigned=True),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "create_time",
            mysql.DATETIME(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=True,
        ),
        sa.Column(
            "update_time",
            mysql.DATETIME(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=True,
        ),
        sa.Column(
            "net_sent",
            mysql.BIGINT(unsigned=True),
            server_default=sa.text("0"),
            nullable=True,
        ),
        sa.Column(
            "net_recv",
            mysql.BIGINT(unsigned=True),
            server_default=sa.text("0"),
            nullable=True,
        ),
        sa.Column(
            "disk_read",
            mysql.BIGINT(unsigned=True),
            server_default=sa.text("0"),
            nullable=True,
        ),
        sa.Column(
            "disk_write",
            mysql.BIGINT(unsigned=True),
            server_default="",
            nullable=True,
        ),
        sa.Column(
            "ts",
            mysql.BIGINT(unsigned=True),
            server_default=sa.text("0"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.execute(
        "insert into flask_state_io_dg_tmp(id, create_time, update_time, net_sent, net_recv, disk_read, disk_write, ts) select id, create_time, update_time, net_sent, net_recv, disk_read, disk_write, ts from flask_state_io;"
    )
    op.drop_table("flask_state_io")
    op.rename_table("flask_state_io_dg_tmp", "flask_state_io")
    op.create_index(
        "idx_ts", "flask_state_io", [sa.text("ts DESC")], unique=False
    )
