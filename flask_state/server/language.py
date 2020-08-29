import logging

from . import MsgCode, LANGUAGE
from .response_methods import make_response_content


def return_language(language) -> dict:
    """
    Return to custom language
    :param language: response data
    :return: flask response
    """
    try:
        if language not in LANGUAGE:
            return make_response_content(MsgCode.NOT_SUPPORT_LANGUAGE)
        data = LANGUAGE[language]
        return make_response_content(data=data)
    except Exception as e:
        logging.error(e)
        return make_response_content(MsgCode.UNKNOWN_ERROR)
