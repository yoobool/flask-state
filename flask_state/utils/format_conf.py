def format_language(language=None):
    if not isinstance(language, str):
        language = str(language)
    return language


def format_id_name(id_name=None):
    if not isinstance(id_name, tuple):
        id_name = (True, '')
    return id_name


def format_sec(secs=None):
    """
    Format incoming time
    :param secs: initial time
    :return: format time
    """
    if not isinstance(secs, int) or secs < 10:
        return 60
    else:
        return secs


def format_address(address=None):
    """
    Format incoming database address
    :param address: initial database address
    :return: format database address
    """
    if not isinstance(address, tuple) or not isinstance(address[0], str) or not isinstance(address[1], int):
        return 'sqlite:///console_host.db'
    res = ''
    for i in range(len(address[0])):
        if address[0][i].isalnum():
            res += address[0][i:]
            break
    res = res.replace('/', '').replace('?', '')
    parent = '../' if address[1] == 1 else ''
    res = 'sqlite:///' + parent + res + '.db'
    return res
