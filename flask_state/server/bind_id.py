import logging

from . import MsgCode
from .response_methods import make_response_content


def send_id(id_name='console_machine_status', ball=True) -> dict:
    """
    Send binding ID
    :param id_name:
    :return:
    """
    try:
        if ball not in (True, False) or not isinstance(id_name, str):
            return make_response_content(MsgCode.ERROR_TYPE)
        data = {'circular': ball, 'id_name': id_name}
        return make_response_content(data=data, msg='ID sent successfully')
    except Exception as e:
        logging.error(e)
        return make_response_content(MsgCode.UNKNOWN_ERROR)
