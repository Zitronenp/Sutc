from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    priority = db.Column(db.String(6), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    steps = db.Column(db.String(80), nullable=False)
    oj_res = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return '<Case %r>' % self.title

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return '<Book %r>' % self.title