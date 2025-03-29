from flask import Flask
from models import Case, db
import json
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cases.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


def create_db():
    with app.app_context():
        # Удаляем все таблицы (если они есть)
        db.drop_all()

        # Создаём новые таблицы
        db.create_all()

        # Загружаем тест-кейсы из JSON
        with open('cases.json', encoding='utf-8') as f:
            cases_data = json.load(f)

        for case_data in cases_data:
            case = Case(
                title=case_data['название'],
                priority=case_data['приоритет'],
                steps=case_data['шаги'],
                oj_res=case_data['ожидаемый результат'],
                description=case_data['описание']
            )
            db.session.add(case)

        db.session.commit()
        print("База данных успешно пересоздана и заполнена!")