## Подготовка окружения к разработке 

Создать в корневой папке файл `.env`. Пример есть в файле `.env.sample`. 

## Запуск
При первом запуске прописать `docker-compose up` с флагом `--build`. 
Для создания суперпользователя прописать `docker-compose run backend ./manage.py createsuperuser`.
Swagger находится на `http://localhost:8000/api/docs/swagger-ui/`

