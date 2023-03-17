from flask import jsonify
from flask_restful import abort, Resource

from . import db_session
from .jobs import Jobs
from .reqparse import add_job_parser, edit_job_parser


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404, message=f"Job {job_id} not found")


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        return jsonify({'job': job.to_dict(
            only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'is_finished'))})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})

    def post(self, job_id):  # редактировать работу
        abort_if_job_not_found(job_id)
        args = edit_job_parser.parse_args()
        session = db_session.create_session()
        if args['id']:
            if session.query(Jobs).get(args['id']) and args['id'] != job_id:
                abort(400, message="Id already exists")
        session.query(Jobs).filter(Jobs.id == job_id).update({k: v for k, v in args.items() if v is not None})
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': [job.to_dict(
            only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'is_finished')) for job in jobs]})

    def post(self):
        args = add_job_parser.parse_args()
        session = db_session.create_session()
        if args['id']:
            if session.query(Jobs).get(args['id']):
                abort(400, message="Id already exists")
        job = Jobs(**{k: v for k, v in args.items() if v is not None})
        session.add(job)
        session.commit()
        return jsonify({'success': 'OK'})
