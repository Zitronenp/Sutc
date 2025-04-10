from flask import Flask, request, render_template, redirect, flash, url_for
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, Case, User, Project

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cases.db'
app.config['SECRET_KEY'] = 'secret-key-goes-here'
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
# связываем приложение и экземпляр SQLAlchemy
#db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('projects.html', user_id=current_user.id)
    else:
        return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already taken')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password, email=email)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully')
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/projects')
@login_required
def projects():
    # Получаем проекты только для текущего пользователя
    user_projects = Project.query.filter_by(author_id=current_user.id).order_by(Project.created_at.desc()).all()
    return render_template('projects.html', projects=user_projects)


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

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        priority = request.form['priority']
        steps = request.form['steps']
        oj_res = request.form['oj_res']
        description = request.form['description']
        new_item = Case(title=title, priority=priority, steps=steps,oj_res=oj_res,description=description)
        db.session.add(new_item)
        db.session.commit()
        return redirect('/')
    return render_template('add.html')


@app.route('/projects/create', methods=['GET', 'POST'])
@login_required
def create_project():
    if request.method == 'POST':
        title = request.form['title']
        new_project = Project(title=title, author_id=current_user.id)
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('projects'))

    return render_template('create_project.html')


@app.route('/projects/<int:project_id>/cases')
@login_required
def project_cases(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('project_cases.html', project=project)


@app.route('/projects/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    if request.method == 'POST':
        project.title = request.form['title']
        db.session.commit()
        return redirect(url_for('projects'))

    return render_template('edit_project.html', project=project)


if __name__ == '__main__':
    app.run(debug=True)