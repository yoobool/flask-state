from ..conf.config import Config
from ..exceptions.log_msg import InfoMsg
from ..models import db
from ..models.flask_state_host import FlaskStateHost
from ..models.flask_state_io import FlaskStateIO
from ..utils.date import get_current_ms, get_query_ms
from ..utils.logger import flask_logger

ONE_DAY = 1  # Days
THIRTY_DAT = 30  # 30 Days
FIVE_MINUTES_MILLISECONDS = 300000  # Five minutes milliseconds


def retrieve_host_status(days) -> list:
    """
    Query the status within the time period and flashback

    """
    target_time = get_current_ms() - get_query_ms(days)
    result = (
        FlaskStateHost.query.with_entities(
            FlaskStateHost.cpu,
            FlaskStateHost.memory,
            FlaskStateHost.load_avg,
            FlaskStateHost.ts,
            FlaskStateHost.cpus,
        )
        .filter(FlaskStateHost.ts > target_time)
        .order_by(FlaskStateHost.ts)
        .all()
    )
    return result


def retrieve_io_status() -> list:
    """
    Query the status within the time period and flashback

    """
    result = (
        FlaskStateHost.query.with_entities(
            FlaskStateIO.disk_read,
            FlaskStateIO.disk_write,
            FlaskStateIO.net_recv,
            FlaskStateIO.net_sent,
            FlaskStateIO.packets_recv,
            FlaskStateIO.packets_sent,
            FlaskStateIO.read_count,
            FlaskStateIO.write_count,
            FlaskStateIO.ts,
        )
        .order_by(FlaskStateIO.ts.desc())
        .limit(Config.MAX_RETURN_RECORDS)
        .all()
    )
    return result


def retrieve_latest_host_status() -> dict:
    """
    Query the latest status

    """
    result = (
        FlaskStateHost.query.with_entities(FlaskStateHost.__table__)
        .order_by(FlaskStateHost.ts.desc())
        .first()
    )
    result = result._asdict() if result else {}
    return result


def retrieve_latest_io_status() -> dict:
    """
    Query the latest io status

    """
    result = (
        FlaskStateIO.query.with_entities(FlaskStateIO.__table__)
        .order_by(FlaskStateIO.ts.desc())
        .first()
    )
    result = result._asdict() if result else {}
    return result


def create_host_status(kwargs):
    """
    Create a new record
    """
    try:
        flask_state_host = FlaskStateHost(**kwargs)
        db.session.add(flask_state_host)
        db.session.commit()
        flask_logger.logger.info(InfoMsg.INSERT_SUCCESS.get_msg())
    except Exception as e:
        db.session.rollback()
        raise e


def create_host_io(kwargs):
    """
    Create a new io record
    """
    try:
        flask_state_io = FlaskStateIO(**kwargs)
        db.session.add(flask_state_io)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


def delete_thirty_days_status():
    """
    Delete thirty days records ago

    """
    try:
        target_time = get_current_ms() - get_query_ms(THIRTY_DAT)
        result = FlaskStateHost.query.filter(
            FlaskStateHost.ts < target_time
        ).delete(synchronize_session=False)
        if result:
            db.session.commit()
            flask_logger.logger.info(InfoMsg.DELETE_SUCCESS.get_msg())
        else:
            db.session.rollback()
    except Exception as e:
        db.session.rollback()
        raise e


def delete_thirty_days_io_status():
    """
    Delete thirty days io records ago

    """
    try:
        target_time = get_current_ms() - get_query_ms(THIRTY_DAT)
        result = FlaskStateIO.query.filter(
            FlaskStateIO.ts < target_time
        ).delete(synchronize_session=False)
        if result:
            db.session.commit()
            flask_logger.logger.info(InfoMsg.DELETE_SUCCESS.get_msg())
        else:
            db.session.rollback()
    except Exception as e:
        db.session.rollback()
        raise e


def retrieve_host_status_yesterday() -> FlaskStateHost:
    """
    Returns the closest time status between yesterday and the current

    """
    yesterday_ms = get_current_ms() - get_query_ms(ONE_DAY)
    delta_ms = yesterday_ms - FIVE_MINUTES_MILLISECONDS
    yesterday_flask_state_host = (
        FlaskStateHost.query.filter(
            FlaskStateHost.ts < yesterday_ms, FlaskStateHost.ts > delta_ms
        )
        .order_by(FlaskStateHost.ts.desc())
        .first()
    )
    return yesterday_flask_state_host
