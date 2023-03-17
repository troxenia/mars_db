from flask import Flask, render_template, make_response, jsonify
from requests import get

from data import db_session, jobs_api, users_api
from data.map_api import get_image

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/mars.db")
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.run()


@app.errorhandler(404)
def not_found(_):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html', title='Mars Colonisation')


@app.route('/users_show/<int:user_id>')
def users_show(user_id):
    user = get(f'http://127.0.0.1:5000/api/users/{user_id}').json()
    if 'user' not in user:
        return user
    with open('static/img/city_from.png', "wb") as file:
        file.write(get_image(user['user']['city_from']).content)
    return render_template('users_show.html', title='Add department',
                           name=f"{user['user']['name']} {user['user']['surname']}",
                           city_from=user['user']['city_from'])


if __name__ == '__main__':
    main()
