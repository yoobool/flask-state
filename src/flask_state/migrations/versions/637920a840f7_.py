import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "637920a840f7"
down_revision = None
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
        "flask_state_host",
        sa.Column(
            "cpus", sa.String(length=128), nullable=True, server_default="[]"
        ),
    )


def downgrade_flask_state_sqlite():
    op.create_table(
        "flask_state_host_dg_tmp",
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
            "cpu",
            mysql.FLOAT(unsigned=True),
            server_default=sa.text("0"),
            nullable=True,
        ),
        sa.Column(
            "memory",
            mysql.FLOAT(unsigned=True),
            server_default=sa.text("0"),
            nullable=True,
        ),
        sa.Column(
            "load_avg", sa.String(length=32), server_default="", nullable=True
        ),
        sa.Column(
            "disk_usage",
            mysql.FLOAT(unsigned=True),
            server_default=sa.text("0"),
            nullable=True,
        ),
        sa.Column(
            "boot_seconds",
            mysql.INTEGER(unsigned=True),
            server_default=sa.text("0"),
            nullable=True,
        ),
        sa.Column(
            "ts",
            mysql.BIGINT(unsigned=True),
            server_default=sa.text("0"),
            nullable=True,
        ),
        sa.Column(
            "used_memory",
            mysql.INTEGER(unsigned=True),
            server_default=sa.text("0"),
            nullable=True,
        ),
        sa.Column(
            "used_memory_rss",
            mysql.INTEGER(unsigned=True),
            server_default=sa.text("0"),
            nullable=True,
        ),
        sa.Column(
            "connected_clients",
            mysql.SMALLINT(unsigned=True),
            server_default=sa.text("0"),
            nullable=True,
        ),
        sa.Column(
            "uptime_in_seconds",
            mysql.INTEGER(unsigned=True),
            server_default=sa.text("0"),
            nullable=True,
        ),
        sa.Column(
            "mem_fragmentation_ratio",
            mysql.FLOAT(unsigned=True),
            server_default=sa.text("0"),
            nullable=True,
        ),
        sa.Column(
            "keyspace_hits",
            mysql.INTEGER(unsigned=True),
            server_default=sa.text("0"),
            nullable=True,
        ),
        sa.Column(
            "keyspace_misses",
            mysql.INTEGER(unsigned=True),
            server_default=sa.text("0"),
            nullable=True,
        ),
        sa.Column(
            "hits_ratio",
            mysql.FLOAT(unsigned=True),
            server_default=sa.text("0"),
            nullable=True,
        ),
        sa.Column(
            "delta_hits_ratio",
            mysql.FLOAT(unsigned=True),
            server_default=sa.text("0"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.execute(
        "insert into flask_state_host_dg_tmp(id, create_time, update_time, cpu, memory, load_avg, disk_usage, boot_seconds, ts, used_memory, used_memory_rss, connected_clients, uptime_in_seconds, mem_fragmentation_ratio, keyspace_hits, keyspace_misses, hits_ratio, delta_hits_ratio) select id, create_time, update_time, cpu, memory, load_avg, disk_usage, boot_seconds, ts, used_memory, used_memory_rss, connected_clients, uptime_in_seconds, mem_fragmentation_ratio, keyspace_hits, keyspace_misses, hits_ratio, delta_hits_ratio from flask_state_host;"
    )
    op.drop_table("flask_state_host")
    op.rename_table("flask_state_host_dg_tmp", "flask_state_host")
    op.create_index(
        "idx_ts", "flask_state_host", [sa.text("ts DESC")], unique=False
    )
