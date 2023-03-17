from requests import get, post, delete

# Получение данных
print(get('http://127.0.0.1:5000/api/v2/users').json())  # get all users
print(get('http://127.0.0.1:5000/api/v2/users/1').json())  # get specific correct user
print(get('http://127.0.0.1:5000/api/v2/users/100').json())  # get incorrect user
print(get('http://127.0.0.1:5000/api/v2/users/q').json())  # incorrect type

# Запись новых данных
# Корректный запрос
print(post('http://127.0.0.1:5000/api/v2/users',
           json={'id': 8,
                 'surname': 'Clawthorne',
                 'name': 'Lilith',
                 'age': 47,
                 'position': 'astronaut',
                 'speciality': 'Chemist',
                 'address': 'module_4',
                 'email': 'covenhead@mail.com',
                 'password': 'curse'}).json())
# Существующий id
print(post('http://127.0.0.1:5000/api/v2/users',
           json={'id': 1,
                 'surname': 'Plantar',
                 'name': 'Polly',
                 'age': 15,
                 'position': 'astronaut',
                 'speciality': 'robotics engineer',
                 'address': 'module_4',
                 'email': 'frobo@mail.com',
                 'password': 'pollywog'}).json())
# Существующий email
print(post('http://127.0.0.1:5000/api/v2/users',
           json={'surname': 'Plantar',
                 'name': 'Polly',
                 'age': 15,
                 'position': 'astronaut',
                 'speciality': 'robotics engineer',
                 'address': 'module_4',
                 'email': 'covenhead@mail.com',
                 'password': 'pollywog'}).json())
# Пустой запрос
print(post('http://127.0.0.1:5000/api/v2/users').json())
# Неполный запрос
print(post('http://127.0.0.1:5000/api/v2/users',
           json={'position': 'astronaut',
                 'speciality': 'Experimental physicist'}).json())
# Получить всех пользователей для проверки
print(get('http://127.0.0.1:5000/api/v2/users').json())

# Удаление данных
print(delete('http://127.0.0.1:5000/api/v2/users/100').json())  # incorrect delete
print(delete('http://127.0.0.1:5000/api/v2/users/q').json())  # incorrect type
print(delete('http://127.0.0.1:5000/api/v2/users/9').json())  # correct delete
print(get('http://127.0.0.1:5000/api/v2/users').json())  # get all users again

# Редактирование данных
print(post('http://127.0.0.1:5000/api/v2/users/11', json={
    'id': 9,
    'email': 'bats@mail.com'}).json())  # correct edit
print(post('http://127.0.0.1:5000/api/v2/users/7', json={
    'name': 'Elizabeth',
    'email': 'bats@mail.com'}).json())  # email already exists
print(post('http://127.0.0.1:5000/api/v2/users/100', json={
    'surname': 'Porter',
    'name': 'Augustus'}).json())  # user doesn't exist
print(post('http://127.0.0.1:5000/api/v2/users/2').json())  # empty request
print(post('http://127.0.0.1:5000/api/v2/users/2', json={
    'id': 1,
    'email': 'snake@mail.com'}).json())  # id already exists
print(get('http://127.0.0.1:5000/api/v2/users').json())  # get all users again
