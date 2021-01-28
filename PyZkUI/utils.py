import logging

from kazoo.client import KazooClient
from kazoo.handlers.threading import KazooTimeoutError
from kazoo.exceptions import KazooException


logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)


def _get(zk_client, path):
    data, stat = zk_client.get(path)
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
    children = zk_client.get_children(path)
    if path == '/':
        children = ['/' + c for c in children]
    else:
        children = [(path + '/' + c) for c in children]
    return {'node': node, 'children': children}


def _delete(zk_client, path):
    zk_client.delete(path, recursive=True)
    return {}


def _add(zk_client, path, data):
    zk_client.create(path, bytes(data, encoding='utf-8'))
    return {}


def zk_node_ops(host, method, **kwargs):
    zk_client = KazooClient(hosts=host)
    method = str(method).lower()
    res = {'status': 'success'}
    try:
        zk_client.start(timeout=kwargs.get('timeout') or 5)
        if method == 'get':
            data = _get(zk_client, kwargs.get('path'))
            res.update(**data)
        elif method == 'delete':
            _delete(zk_client, kwargs.get('path'))
        elif method == 'add':
            _add(zk_client, kwargs.get('path'), kwargs.get('data'))
        elif method == 'check':
            pass
        else:
            raise ValueError('Unsupported ZK Method [{}]'.format(method.upper()))
    except KazooTimeoutError:
        logger.error('Failed to connect {}'.format(host))
        res = {'status': 'failed', 'message': 'Failed to connect host due to TimeOut.'}
    except KazooException as e:
        res = {'status': 'failed', 'message': 'Failed to {} node due to KazooException({}).'.format(method, repr(e))}
    finally:
        zk_client.stop()
        zk_client.close()
        return res



