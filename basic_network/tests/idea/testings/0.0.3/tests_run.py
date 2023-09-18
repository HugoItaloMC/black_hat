from tests_bind import SenderBind
from tests_conn import SenderConn
from tests_parser import JoinParser

_args = JoinParser()
_bind = SenderBind()
_conn = SenderConn()


def run() -> None:
    _parser = _args()

    if _parser['listen']:
        _bind.start_process(_parser['target'], _parser['port'])

    elif not _parser['listen'] and len(_parser['target']) and _parser['port'] > 0:
        _conn.start_process(_parser['target'], _parser['port'])


if __name__ == '__main__':
    run()
