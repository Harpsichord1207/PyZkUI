import time

from kazoo.client import KazooClient


class HostHistory:

    def __init__(self, lmt=5):
        self._data = {}

    def accept(self, host):
        self._data[host] = time.time()

    def export(self):
        ...


def get_zk_nodes(host, port=2181):
    zk = KazooClient(hosts='{}:{}'.format(host, port))
    zk.start()

    def _recursive(_path):
        print(_path)
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
    import time
    s = time.time()
    data = _recursive('/')['nodes']
    print(time.time() -s )
    return data
