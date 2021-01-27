import logging

from kazoo.client import KazooClient
from kazoo.handlers.threading import KazooTimeoutError
from kazoo.exceptions import KazooException


logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)


def delete_zk_node(host, path):
    zk = KazooClient(hosts=host)
    try:
        zk.start(timeout=5)
        zk.delete(path, recursive=True)
        return {'status': 'success'}
    except KazooTimeoutError:
        logger.error('Failed to connect {}'.format(host))
        return {'status': 'failed', 'message': 'Failed to connect host due to TimeOut.'}
    except KazooException as e:
        logger.error(repr(e))
        return {'status': 'failed', 'message': 'Failed to create node due to {}'.format(repr(e))}
    finally:
        zk.stop()
        zk.close()


def add_zk_node(host, path, data):
    zk = KazooClient(hosts=host)
    try:
        zk.start(timeout=5)
        zk.create(path, bytes(data, encoding='utf-8'))
        return {'status': 'success'}
    except KazooTimeoutError:
        logger.error('Failed to connect {}'.format(host))
        return {'status': 'failed', 'message': 'Failed to connect host due to TimeOut.'}
    except KazooException as e:
        # TODO: update node if exists
        logger.error(repr(e))
        return {'status': 'failed', 'message': 'Failed to create node due to {}'.format(repr(e))}
    finally:
        zk.stop()
        zk.close()


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
        zk.stop()
        zk.close()
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
