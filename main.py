from flask import Flask, render_template, redirect, abort, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data.users import User
from data.jobs import Jobs
from data.departments import Department
from data import db_session
from forms.user import RegisterForm, LoginForm, JobsForm, DepartmentForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/mars.db")
    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    users = db_sess.query(User).all()
    names = {user.id: (user.surname, user.name) for user in users}
    return render_template("index.html", jobs=jobs, names=names)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.surname = form.surname.data
        user.name = form.name.data
        user.email = form.email.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


# Jobs actions
@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs(team_leader=form.team_leader.data, job=form.job.data, work_size=form.work_size.data,
                   collaborators=form.collaborators.data, is_finished=int(form.is_finished.data))
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('job.html', title='Add job', form=form)


@app.route('/edit_job/<int:job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    form = JobsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == job_id) \
            .filter((Jobs.team_leader == current_user.id) | (current_user.id == 1)).first()
        if job:
            form.team_leader.data = job.team_leader
            form.job.data = job.job
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.is_finished.data = job.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == job_id) \
            .filter((Jobs.team_leader == current_user.id) | (current_user.id == 1)).first()
        if job:
            job.team_leader = form.team_leader.data
            job.job = form.job.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('job.html', title='Edit job', form=form)


@app.route('/delete_job/<int:job_id>', methods=['GET', 'POST'])
@login_required
def delete_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id) \
        .filter((Jobs.team_leader == current_user.id) | (current_user.id == 1)).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


# Departments actions
@app.route("/departments")
def departments_list():
    db_sess = db_session.create_session()
    departments = db_sess.query(Department).all()
    users = db_sess.query(User).all()
    names = {user.id: (user.surname, user.name) for user in users}
    return render_template("departments.html", departments=departments, names=names)


@app.route('/add_department', methods=['GET', 'POST'])
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        department = Department(title=form.title.data, chief=form.chief.data, members=form.members.data,
                                email=form.email.data)
        db_sess.add(department)
        db_sess.commit()
        return redirect('/departments')
    return render_template('department.html', title='Add department', form=form)


@app.route('/edit_department/<int:department_id>', methods=['GET', 'POST'])
def edit_department(department_id):
    form = DepartmentForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        department = db_sess.query(Department).filter(Department.id == department_id) \
            .filter((Department.chief == current_user.id) | (current_user.id == 1)).first()
        if department:
            form.title.data = department.title
            form.chief.data = department.chief
            form.members.data = department.members
            form.email.data = department.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        department = db_sess.query(Department).filter(Department.id == department_id) \
            .filter((Department.chief == current_user.id) | (current_user.id == 1)).first()
        if department:
            department.title = form.title.data
            department.chief = form.chief.data
            department.members = form.members.data
            department.email = form.email.data
            db_sess.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('department.html', title='Edit department', form=form)


@app.route('/delete_department/<int:department_id>', methods=['GET', 'POST'])
@login_required
def delete_department(department_id):
    db_sess = db_session.create_session()
    department = db_sess.query(Department).filter(Department.id == department_id) \
        .filter((Department.chief == current_user.id) | (current_user.id == 1)).first()
    if department:
        db_sess.delete(department)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/departments')


if __name__ == '__main__':
    main()
