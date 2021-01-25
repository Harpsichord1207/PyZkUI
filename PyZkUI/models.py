from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError


db = SQLAlchemy()


class ZK(db.Model):

    __tablename__ = 'zk'

    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String(256), unique=True, nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return '<Zookeeper: %r>' % self.host

    def save(self):
        db.session.add(self)
        try:
            db.session.flush()
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'status': 'failed', 'message': str(e)}
        return {'time': self.time, 'host': self.host, 'id': self.id, 'status': 'success'}

    @classmethod
    def export(cls):
        return [
            {'time': zk.time, 'host': zk.host, 'id': zk.id} for zk in cls.query.all()
        ]

    @classmethod
    def get_by_id(cls, zk_id):
        return cls.query.filter_by(id=int(zk_id)).first()

    @classmethod
    def delete(cls, zk_id):
        me = cls.get_by_id(zk_id=zk_id)
        db.session.delete(me)
        db.session.commit()
