### Сервис для работы с CSV файлами через API

Сервис развернут на сервере. 
По адресу http://80.249.146.118:5000/swagger/ - можно посмотреть документацию к API в формате OpenAPI.

***Инструкция для запуска локально***

 В командах использовать python3 для macOS, Linux. python для Windows.

1. Склонировать репозиторий `git clone https://github.com/MalkovGN/csv_service`
2. Перейти в папку проекта, создать виртуальное окружение: `python3 -m venv env`
3. Активировать окружение и установить зависимоти: `pip3 install -r requirements.txt`
4. Применить миграции в базу данных: `python3 manage.py migrate`
5. Запустить сервер: `python3 manage.py runserver`
6. Открыть в браузере адрес http://127.0.0.1:8000/swagger/ для просмотра эндпоинтов.
 
***Описание эндпоинтов***
1. /api/v1/files_info/ - список всех загруженных файлов, с информацией о наименованиях колонок в них. Метод GET.
2. /api/v1/upload_file/ - загрузка файла (перейти в HTML form для отображения кнопки выбора файла). Метод POST.
3. /api/v1/file/{id}/ - данные из файла с id={id}. Метод GET.
4. /api/v1/file/{id}/?colomns=column_name1,column_name2 - для сортировки данных по одному или нескольким стоблцам CSV-файла. Метод GET.
5. /api/v1/file/{id}/ - удаление файла с id={id}. Метод DELETE.
