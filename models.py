from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# Таблица связи многие-ко-многим: пользователи и проекты
user_project = db.Table('user_project',
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                        db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True)
                        )

# Таблица связи многие-ко-многим: проекты и тест-кейсы
project_case = db.Table('project_case',
                        db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True),
                        db.Column('case_id', db.Integer, db.ForeignKey('case.id'), primary_key=True)
                        )


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Связи
    projects = db.relationship('Project', secondary=user_project, back_populates='users')
    created_projects = db.relationship('Project', back_populates='author', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Связи
    author = db.relationship('User', back_populates='created_projects')
    users = db.relationship('User', secondary=user_project, back_populates='projects')
    cases = db.relationship('Case', secondary=project_case, back_populates='projects', cascade='all, delete')

    def __repr__(self):
        return f'<Project {self.title}>'


class Case(db.Model):
    __tablename__ = 'case'
    id = db.Column(db.Integer, primary_key=True)
    priority = db.Column(db.String(6), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    steps = db.Column(db.String(500), nullable=False)  # Увеличил длину для хранения всех шагов
    oj_res = db.Column(db.String(200), nullable=False)  # Увеличил длину
    description = db.Column(db.String(1000), nullable=False)  # Увеличил длину

    # Связи
    projects = db.relationship('Project', secondary=project_case, back_populates='cases')

    def __repr__(self):
        return f'<Case {self.title}>'