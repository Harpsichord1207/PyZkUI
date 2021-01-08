import datetime
import logging
import time

from kazoo.client import KazooClient
from kazoo.handlers.threading import KazooTimeoutError


logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)


class HostList:

    data = []

    @classmethod
    def add(cls, host):
        _id = len(cls.data) + 1
        host_obj = {
            'time': str(datetime.datetime.now())[:22],
            'host': host
        }
        cls.data.append(host_obj)
        return {**host_obj, 'id': _id}

    @classmethod
    def export(cls):
        return [{**ele, 'id': i+1} for i, ele in enumerate(cls.data)]


def check_zk_host(host, timeout=1):
    zk = KazooClient(host)
    try:
        zk.start(timeout=timeout)
        logger.info('Connect to {}'.format(host))
        zk.stop()
        zk.close()
    except KazooTimeoutError:
        logger.error('Failed to connect {}'.format(host))
        return False
    return True


def get_zk_node(host, path='/'):
    zk = KazooClient(hosts=host)
    try:
        zk.start(timeout=5)
    except KazooTimeoutError:
        logger.error('Failed to connect {}'.format(host))
        return
    data, stat = zk.get(path)
    node = {
        'data': str(data)[1:].strip("'"),
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
    children = zk.get_children(path)
    if path == '/':
        children = ['/' + c for c in children]
    else:
        children = [(path + '/' + c) for c in children]
    zk.stop()
    zk.close()
    return node, children


def get_zk_nodes(host):
    zk = KazooClient(hosts=host)
    try:
        zk.start(timeout=5)
    except KazooTimeoutError:
        logger.error('Failed to connect {}'.format(host))
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
    zk.stop()
    zk.close()
    return data
