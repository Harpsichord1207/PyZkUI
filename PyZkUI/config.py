import pathlib
import uuid

ROOT_PATH = pathlib.Path(__file__).parent.resolve()

ROOT_PATH.joinpath('db').mkdir(exist_ok=True)
_sql_lite_file = ROOT_PATH.joinpath('db').joinpath('sqlite.db').resolve()


class FlaskConfig:

    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(_sql_lite_file)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = uuid.uuid4().hex
