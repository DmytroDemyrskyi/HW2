import csv

import requests
from faker import Faker
from flask import Flask, request

app = Flask(__name__)


@app.route('/requirements/')
def requirements():
    with open('requirements.txt', 'r') as file:
        read_file = file.read()
    content = read_file.replace('\n', '<br>')
    return content


@app.route('/users/generate')
def people_generator():
    content = ''
    fake = Faker("ru_RU")
    i = 1
    count = request.args.get('count', '100')
    try:
        count = int(count)
        if 0 < count <= 10000:
            while i <= count:
                first_name = fake.first_name()
                email = fake.ascii_free_email()
                content += str(i) + '. ' + first_name + ' ' + email + '<br>'
                i = i + 1
        else:
            content = 'Ошибка. Введите число от 1 до 10000'
    except ValueError:
        content = 'Ошибка. Введите числовое значение'

    return content


@app.route('/mean/')
def average_value():
    height = 0
    weight = 0
    row_count = 0
    with open('hw.csv', 'r') as file:
        data = csv.reader(file)

        for row in data:
            if len(row) >= 2:
                column1_data = row[1]
                column2_data = row[2]

                try:
                    column1_data = float(column1_data)
                    column2_data = float(column2_data)

                    height += column1_data
                    weight += column2_data

                    row_count += 1
                except ValueError:
                    print('Ошибка: невозможно преобразовать строку в число')

        height = (height / row_count) * 2.54
        weight = (weight / row_count) * 0.453592

        content = 'Середній зріст: ' + str(int(height)) + ' см' + '<br>Середня вага: ' + str(int(weight)) + ' кг'

    return content


@app.route('/space/')
def space():
    response = requests.get('http://api.open-notify.org/astros.json')

    if response.status_code == 200:
        data = response.json()
        number = data['number']
        content = 'Прямо сейчас на орбите ' + str(number) + ' космонавтов!'
    else:
        content = 'Запрос не удался. Попробуйте снова'

    return content
