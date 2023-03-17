import flask
from flask import request, jsonify

from . import db_session
from .jobs import Jobs

blueprint = flask.Blueprint('jobs_api', __name__, template_folder='templates')


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {'jobs': [job.to_dict(only=('id', 'team_leader', 'job', 'work_size', 'collaborators',
                                    'start_date', 'end_date', 'is_finished')) for job in jobs]})


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    return jsonify({'job': job.to_dict(only=('id', 'team_leader', 'job', 'work_size', 'collaborators',
                                             'start_date', 'end_date', 'is_finished'))})


@blueprint.route('/api/jobs', methods=['POST'])
def add_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['team_leader', 'job', 'work_size', 'collaborators', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    if 'id' in request.json:
        if request.json['id'] in tuple(job.id for job in db_sess.query(Jobs).all()):
            return jsonify({'error': 'Id already exists'})
    job = Jobs(**request.json)
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    db_sess.delete(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['POST'])
def edit_job(job_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in ['id', 'team_leader', 'job', 'work_size', 'collaborators', 'is_finished'] for key in
                 request.json):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    job_to_edit = db_sess.query(Jobs).get(job_id)
    if not job_to_edit:
        return jsonify({'error': 'Not found'})
    if 'id' in request.json:
        if request.json['id'] in tuple(job.id for job in db_sess.query(Jobs).all() if job_to_edit.id != job.id):
            return jsonify({'error': 'Id already exists'})
    db_sess.query(Jobs).filter(Jobs.id == job_id).update(request.json)
    db_sess.commit()
    return jsonify({'success': 'OK'})
