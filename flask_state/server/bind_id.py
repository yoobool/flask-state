from .response_methods import make_response_content


def send_id(id_name=(True, 'console_machine_status')) -> dict:
    """
    Send binding ID
    :param id_name:
    :return:
    """
    try:
        data = {'circular': id_name[0], 'id_name': id_name[1]}
        return make_response_content(data=data, msg='ID sent successfully')
    except Exception as e:
        raise e
