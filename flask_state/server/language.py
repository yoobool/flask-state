import logging
from . import MsgCode, LANGUAGE
from ..utils.format_conf import format_language
from .response_methods import make_response_content


def return_language(language='Chinese') -> dict:
    """
    Return to custom language
    :param language: response data
    :return: flask response
    """
    try:
        language = format_language(language)
        if language not in LANGUAGE:
            return make_response_content(MsgCode.NOT_SUPPORT_LANGUAGE)
        data = LANGUAGE[language]
        return make_response_content(data=data)
    except Exception as e:
        logging.error(e)
        return make_response_content(MsgCode.UNKNOWN_ERROR)
