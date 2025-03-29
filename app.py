from flask import Flask, render_template
from models import Case, db
from create_db_cases import create_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cases.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# связываем приложение и экземпляр SQLAlchemy
db.init_app(app)

@app.route('/')
def index():
    return render_template('projects.html')


@app.route('/cases')
def cases():
    cases = Case.query.all()
    return render_template('cases.html', cases=cases)

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/case/<int:case_id>')
def case_detail(case_id):
    case = Case.query.get_or_404(case_id)
    return render_template('case.html', case=case)

if __name__ == '__main__':
    create_db()
    app.run(debug=True)