import argparse
from . import app


if __name__ == '__main__':
    # TODO: Debug Mode
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Host, default is 127.0.0.1', default='127.0.0.1')
    parser.add_argument('--port', help='Port, default is 8088', default=8088, type=int)
    args = parser.parse_args()
    app.run(host=args.host, port=args.port)
