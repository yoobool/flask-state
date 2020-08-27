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


def format_address(address):
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
