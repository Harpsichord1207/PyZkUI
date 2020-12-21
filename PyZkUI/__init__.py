import argparse

from PyZkUI.run import app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Host, default is 127.0.0.1', default='127.0.0.1', type=str)
    parser.add_argument('--port', help='Port, default is 8088', default=8088, type=int)
    parser.add_argument('--debug', help='Debug, default is False', default=False, type=bool)
    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug=args.debug)
