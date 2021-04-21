class Config:
    """ Config """

    REDIS_CONNECT_TIMEOUT = 3  # Redis socket connection timeout
    REDIS_TIMEOUT = 5  # Redis socket timeout
    CPU_PERCENT_INTERVAL = (
        0  # Time interval to calculate CPU utilization using psutil
    )
    DEFAULT_BIND_SQLITE = (
        "flask_state_sqlite"  # Default binding database URL key
    )
    DEFAULT_HITS_RATIO = 100  # Default hits ratio value
    DEFAULT_DELTA_HITS_RATIO = 100  # Default 24h hits ratio value
    DEFAULT_WINDOWS_LOAD_AVG = (
        "0, 0, 0"  # Windows system cannot calculate load AVG
    )
    MAX_RETURN_RECORDS = 480  # Return the maximum number of records
    ABANDON_THRESHOLD = 60  # Maximum timeout time of scheduled tasks
    ABANDON_IO_THRESHOLD = 10  # Maximum timeout time of scheduled tasks
    ALEMBIC_VERSION = "alembic_version"  # alembic table name
    DB_VERSION = "b6b1ecfc9524"  # the last db version
