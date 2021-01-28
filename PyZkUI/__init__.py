import argparse
import waitress


def init_app():
    from PyZkUI.config import FlaskConfig
    from PyZkUI.views import app

    # init db
    from PyZkUI.models import db
    app.config.from_object(FlaskConfig)
    db.init_app(app)
    db.create_all(app=app)

    return app


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Host, default is 127.0.0.1', default='127.0.0.1', type=str)
    parser.add_argument('--port', help='Port, default is 8088', default=8088, type=int)
    parser.add_argument('--threads', help='Threads number, default is 2', default=2, type=int)
    parser.add_argument('--debug', help='Debug, default is False', default=False, type=bool)
    return parser.parse_args()


def main():
    args = parse_args()
    app = init_app()
    if args.debug:
        app.run(host=args.host, port=args.port, debug=True)
    else:
        waitress.serve(app, host=args.host, port=args.port, threads=args.threads)


if __name__ == '__main__':
    main()
