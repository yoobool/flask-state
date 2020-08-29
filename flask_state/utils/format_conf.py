def format_language(language):
    if not isinstance(language, str):
        language = str(language)
    return language


def format_id_name(element, ball=True):
    if ball not in (True, False):
        ball = True
    if not isinstance(element, str):
        element = str(element)
    return element, ball


def format_sec(secs):
    """
    Format incoming time
    :param secs: initial time
    :return: format time
    """
    if not isinstance(secs, int) or secs < 10:
        return 60
    else:
        return secs


def format_address(address, catalogue=0):
    """
    Format incoming database address
    :param address: initial database address
    :return: format database address
    """
    if not isinstance(address, str):
        address = str(address)
    if catalogue not in (0, 1):
        catalogue = 0
    res = ''
    for i in range(len(address)):
        if address[i].isalnum():
            res += address[i:]
            break
    res = res.replace('/', '').replace('?', '')
    parent = '../' if catalogue == 1 else ''
    res = 'sqlite:///' + parent + res
    return res
