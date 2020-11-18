class Config:
    """ Config """

    REDIS_TIMEOUT = 1  # Redis connection timeout
    CPU_PERCENT_INTERVAL = 0  # Time interval to calculate CPU utilization using psutil
    DEFAULT_BIND_SQLITE = "flask_state_sqlite"  # Default binding database URL key
    DEFAULT_HITS_RATIO = 100  # Default hits ratio value
    DEFAULT_DELTA_HITS_RATIO = 100  # Default 24h hits ratio value
    DEFAULT_WINDOWS_LOAD_AVG = "0, 0, 0"  # Windows system cannot calculate load AVG
    MAX_RETURN_RECORDS = 480  # Return the maximum number of records
