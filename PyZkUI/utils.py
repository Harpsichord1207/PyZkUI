import logging
import time

from kazoo.client import KazooClient
from kazoo.handlers.threading import KazooTimeoutError


logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)


class HostHistory:

    def __init__(self, lmt=5):
        self._data = {}

    def accept(self, host):
        self._data[host] = time.time()

    def export(self):
        ...


def get_zk_node(host, port=2181, path='/'):
    zk = KazooClient(hosts='{}:{}'.format(host, port))
    try:
        zk.start(timeout=5)
    except KazooTimeoutError:
        logger.error('Connection Failed: {}:{}'.format(host, port))
        return
    data, stat = zk.get(path)
    node = {
        'data': str(data)[1:],
        'czxid': stat.czxid,
        'mzxid': stat.mzxid,
        'ctime': stat.ctime,
        'mtime': stat.mtime,
        'version': stat.version,
        'cversion': stat.cversion,
        'aversion': stat.aversion,
        'ephemeralOwner': stat.ephemeralOwner,
        'dataLength': stat.dataLength,
        'numChildren': stat.numChildren,
        'pzxid': stat.pzxid
    }
    return node


def get_zk_nodes(host, port=2181):
    zk = KazooClient(hosts='{}:{}'.format(host, port))
    try:
        zk.start(timeout=5)
    except KazooTimeoutError:
        logger.error('Connection Failed: {}:{}'.format(host, port))
        return

    def _recursive(_path):
        logger.info(_path)
        _children = zk.get_children(_path)
        if _path != '/':
            _children_full_path = [(_path + '/' + _c) for _c in _children]
        else:
            _children_full_path = [('/' + _c) for _c in _children]
        _data, _stat = zk.get(_path)

        _children_nodes = [_recursive(_cfp) for _cfp in _children_full_path]
        _res = {
            'text': _path
        }
        if _children_nodes:
            _res['nodes'] = _children_nodes
            _res['icon'] = 'fa fa-folder-open'
        else:
            _res['icon'] = 'fa fa-file-code-o'
        return _res

    _s = time.time()
    data = _recursive('/')['nodes']
    logger.critical('using {:.2f}s'.format(time.time()-_s))
    return data
