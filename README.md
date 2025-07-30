#  Запуск проекта с помощью Docker Compose

## Предварительные требования:
- установлены Docker, Docker Compose
- создан .env файл с переменными окружения

## Шаги для запуска:
1. Клонируйте репозиторий
    ```bash
    git clone https://github.com/your-username/your-repo.git 
    cd your-repo
2. Создайте .env файл в корне проекта и добавьте в него:

    POSTGRES_DB=your_db
    POSTGRES_USER=your_user
    POSTGRES_PASSWORD=your_password
    SECRET_KEY=your_django_secret
    DEBUG=1

3. Соберите и запустите проект
    docker-compose up --build

## Проверка работы
- Проект доступен по адресу: http://localhost:8000
- 
## Компоненты проекта:

- web (Django приложение)
- db (PostgreSQL база данных)
- redis (Брокер сообщений для Celery)
- celery (Воркер Celery)
- celery-beat (Планировщик периодических задач Celery)

## Проверка работы сервисов
- Django (web)
  docker-compose exec web python manage.py migrate
  docker-compose exec web python manage.py createsuperuser
  Перейдите в админку: http://localhost:8000/admin
  Убедитесь, что фронтэнд работает и база данных подключена

- PostgreSQL
  проверьте доступность базы (подставить значения)
  docker-compose exec db psql -U $POSTGRES_USER -d $POSTGRES_DB

- Redis
  проверьте, что Redis работает
  docker-compose exec redis redis-cli ping

- Celery
  проверьте, что Celery воркер запущен и подключен к Redis
  docker-compose logs celery

- Celery Beat
  проверьте, что задачи планировщика запускаются
  docker-compose logs celery-beat
  
## Остановка и удаление контейнеров
    docker-compose down
## Полное удаление с volumes:
    docker-compose down -v
