# Dating
Приложение для знакомств

# Запуск проекта

1) Создаем директорию для проекта и переходим в него  

2) Клонируем репозиторий с gitlab:  

`git init`  

`git clone https://github.com/PolDyy/Dating.git`

3) Создаем и активируем виртуальное окружение в корне проекта:  

`python -m venv venv`

`source venv/bin/activate`

4) Установим зависимотси: 

`python -m pip --upgrade pip`

`pip install -r requirements.txt`

5) Создаем файл .env на основе env_example

6) Проводим миграции:

`python manage.py migrate`


7) Запускаем:

`python manage.py runserver`

Все готово!

## Запуск с помощью Docker

1) Создаем директорию для проекта и переходим в него  

2) Клонируем репозиторий с gitlab:  

`git init`  

`git clone https://github.com/PolDyy/Dating.git`

3) Создаем файл .env на основе env_example

4)  Проверяем установлен ли докер, если нет, то устанавливаем его  
(обратитесь к документации Docker)

5)  Собираем образ по Dockerfile

`sudo docker build -t dating .`

6)  Запускаем приложение:

`docker run -p 8080:8080 dating `

Все готово!

### Эндпоинты

|   | uri                                                | Methods |       Access level | Description                                 |
|---|----------------------------------------------------|:-------:|-------------------:|---------------------------------------------|
| 1 | /api/list                                          |   GET   |          all users | Для получения всех пользователей            |
| 2 | /api/list?first_name=&last_name=&gender=&distance= |   GET   |          all users | Для получения отфильтрованных пользователей |
| 3 | /api/clients/create                                |  POST   |          all users | Для создания аккаунта                       |
| 4 | /api/clients/<int:id>/match                        |   GET   |          all_users | Для получения профиля пользователя          |
| 5 | /api/clients/<int:id>/match                        |  POST   | auth, not_yourself | Для оценивания пользователя                 |
| 6 | /api/auth/login                                    |  POST   |          all_users | Для аутентификации                          |
| 7 | /api/auth/logout                                   |  POST   |               auth | Для выхода из аккаунта                      |
    
    

    Для проверки проекта можете воспользоваться следующим URL: 
    http://poldy.pythonanywhere.com/    
