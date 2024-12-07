import os
import requests
from typing import Optional
import uvicorn
from fastapi import FastAPI
import json


path_to_json = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'students.json')

def json_to_dict_list(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            json_serial = f.read()
            dict_list = json.loads(json_serial)
            return dict_list
    except (TypeError, ValueError, IOError) as e:
        print(f'Ошибка при чтении JSON из файла или преобразовании в список словарей: {e}')
        return None

app = FastAPI()

@app.get("/")
async def root(name: Optional[str] = 'noname', message: Optional[str] = None):
    return f'{name}, {message}'

@app.get("/students/{course}")
def get_all_students_course(course: int, major: Optional[str] = None, enrollment_year: Optional[int] = 2018):
    students = json_to_dict_list(path_to_json)
    filtered_students = []
    for student in students:
        if student["course"] == course:
            filtered_students.append(student)

    if major:
        filtered_students = [student for student in filtered_students if student['major'].lower() == major.lower()]

    if enrollment_year:
        filtered_students = [student for student in filtered_students if student['enrollment_year'] == enrollment_year]

    return filtered_students

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)


r = requests.get('https://api.github.com/events')
req = requests.get('https://api.github.com', auth=('user', 'pass'))
print(req.status_code)
print(req.headers['content-type'])


#module os в нашем предоставляет функции для работы с путями в операционной системе
#module requests дает возможность обращаться к HTTP-запросам
#module typing обеспечивает поддержку подсказок типа во время выполнения, в нашем случаи мы использ. функцию Optional,
# то есть не обязательный аргумент.
#module uvicorn это реализация веб-сервера ASGI для Python и FastAPI работает через него, в нашем случае uvicorn имеет
# метод run для запуска сервера без использ. терминала
#module FastAPI это фреймворк для создания API на языке Python, он обрабатывает запросы url адреса с определенным хостом
# и порто и второй декоратор для обработки этого же url только с параметрами после слэша /
#module json используется для работы с json форматом файлов, а также сериализации


