from flask import Flask
from flask_restful import Api

from data import db_session, users_resourse, jobs_resourse


app = Flask(__name__)
api = Api(app, catch_all_404s=True)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/mars.db")
    api.add_resource(users_resourse.UsersListResource, '/api/v2/users')
    api.add_resource(users_resourse.UsersResource, '/api/v2/users/<int:user_id>')
    api.add_resource(jobs_resourse.JobsListResource, '/api/v2/jobs')
    api.add_resource(jobs_resourse.JobsResource, '/api/v2/jobs/<int:job_id>')
    app.run()


if __name__ == '__main__':
    main()
