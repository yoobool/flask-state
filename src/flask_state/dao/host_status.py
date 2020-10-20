import sys

from ..exceptions.log_msg import InfoMsg
from ..models import db
from ..models.flask_state_host import FlaskStateHost
from ..utils.date import get_current_ms, get_query_ms
from ..utils.format_conf import get_file_inf
from ..utils.logger import logger

ONE_DAY = '1'  # Days
FIVE_MINUTES_MILLISECONDS = 300000  # Five minutes milliseconds


def retrieve_host_status(days) -> list:
    """
    Query the status within the time period and flashback

    """
    target_time = get_current_ms() - get_query_ms(days)
    result = FlaskStateHost.query.filter(FlaskStateHost.ts > target_time).order_by(FlaskStateHost.ts.desc()).all()
    return result


def create_host_status(kwargs):
    """
    Create a new record

    """
    try:
        flask_state_host = FlaskStateHost(**kwargs)
        db.session.add(flask_state_host)
        db.session.commit()
        logger.info(InfoMsg.INSERT_SUCCESS.get_msg(), extra=get_file_inf(sys._getframe()))
    except Exception as e:
        db.session.rollback()
        raise e


def retrieve_host_status_yesterday() -> FlaskStateHost:
    """
    Returns the closest time status between yesterday and the current

    """
    yesterday_ms = get_current_ms() - get_query_ms(ONE_DAY)
    delta_ms = yesterday_ms - FIVE_MINUTES_MILLISECONDS
    yesterday_flask_state_host = FlaskStateHost.query.filter(
        FlaskStateHost.ts < yesterday_ms, FlaskStateHost.ts > delta_ms).order_by(
        FlaskStateHost.ts.desc()).first()
    return yesterday_flask_state_host
