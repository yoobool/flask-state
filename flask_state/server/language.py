from . import MsgCode, LANGUAGE
from .response_methods import make_response_content


def return_language(language='Chinese') -> dict:
    """
    Return to custom language
    :param language: response data
    :return: flask response
    """
    try:
        if language not in LANGUAGE:
            make_response_content(MsgCode.NOT_SUPPORT_LANGUAGE)
        data = LANGUAGE[language]
        return make_response_content(data=data)
    except Exception as e:
        raise e
