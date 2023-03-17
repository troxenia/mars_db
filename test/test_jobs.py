from requests import get, post, delete

# Получение данных
print(get('http://127.0.0.1:5000/api/v2/jobs').json())  # get all jobs
print(get('http://127.0.0.1:5000/api/v2/jobs/1').json())  # get specific correct job
print(get('http://127.0.0.1:5000/api/v2/jobs/100').json())  # get incorrect job
print(get('http://127.0.0.1:5000/api/v2/jobs/q').json())  # incorrect type

# Запись новых данных
# Корректный запрос
print(post('http://127.0.0.1:5000/api/v2/jobs',
           json={'collaborators': '3, 9, 12',
                 'id': 4,
                 'is_finished': False,
                 'job': 'Run experiments on the particle accelerator',
                 'team_leader': 2,
                 'work_size': 5}).json())
# Существующий id
print(post('http://127.0.0.1:5000/api/v2/jobs',
           json={'collaborators': '3, 4, 9',
                 'id': 4,
                 'is_finished': False,
                 'job': 'Grow gene-modified plants',
                 'team_leader': 5,
                 'work_size': 5}).json())
# Пустой запрос
print(post('http://127.0.0.1:5000/api/v2/jobs').json())
# Неполный запрос
print(post('http://127.0.0.1:5000/api/v2/jobs',
           json={'id': 5,
                 'is_finished': False}).json())
# Получить все работы для проверки
print(get('http://127.0.0.1:5000/api/v2/jobs').json())

# Удаление данных
print(delete('http://127.0.0.1:5000/api/v2/jobs/100').json())  # incorrect delete
print(delete('http://127.0.0.1:5000/api/v2/jobs/q').json())  # incorrect type
print(delete('http://127.0.0.1:5000/api/v2/jobs/4').json())  # correct delete
print(get('http://127.0.0.1:5000/api/v2/jobs').json())  # get all jobs again

# Редактирование данных
print(post('http://127.0.0.1:5000/api/v2/jobs/2', json={
    'id': 5,
    'work_size': 10}).json())  # correct edit
print(post('http://127.0.0.1:5000/api/v2/jobs/100', json={
    'job': 'Design a new ventilation system',
    'team_leader': 3}).json())  # job doesn't exist
print(post('http://127.0.0.1:5000/api/v2/jobs/1').json())  # empty request
print(post('http://127.0.0.1:5000/api/v2/jobs/1', json={
    'id': 5,
    'collaborators': '2, 3, 11'}).json())  # id already exists
print(get('http://127.0.0.1:5000/api/v2/jobs').json())  # get all jobs again
