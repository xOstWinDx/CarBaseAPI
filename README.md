## Приложение на FastAPI

Это приложение на FastAPI позволяет пользователям регистрироваться, аутентифицироваться и авторизовываться. Пользователи могут добавлять автомобили, выполнять поиск по автомобилям с использованием фильтров и пагинации, а также, если у них есть права администратора, удалять и изменять существующие в базе данных автомобили.

### Функциональные возможности

- **Регистрация пользователей**: Создание нового пользовательского аккаунта.
- **Аутентификация**: Вход в систему с использованием учетных данных.
- **Авторизация**: Обеспечение наличия у пользователей соответствующих прав доступа.
- **Управление автомобилями**: Добавление, удаление и изменение автомобилей в базе данных.
- **Поиск автомобилей**: Поиск автомобилей с использованием различных фильтров и пагинации.
---

- \* Что бы получить права администратора нужно вручную поставить флаг в БД.
### Начало работы

Вы можете запустить это приложение локально или с использованием Docker. Следуйте приведенным ниже инструкциям для начала работы.

---

### Запуск локально

1. **Копирование и настройка переменных окружения**:
   - Скопируйте файл окружения-примера `.env-example` в `.env`:
     ```bash
     cp .env-example .env
     ```
   - Замените переменные в файле `.env` на ваши собственные данные.

2. **Установка зависимостей**:
   - Установите зависимости проекта с флагом для разработки:
     ```bash
     poetry install --with dev
     ```

3. **Запуск миграций Alembic**:
   - Примените миграции базы данных с использованием Alembic:
     ```bash
     alembic upgrade head
     ```

4. **Запуск приложения**:
   - Запустите приложение FastAPI с использованием Uvicorn:
     ```bash
     uvicorn src.main:app --host 0.0.0.0 --port 8000
     ```

5. **Документация**:
   - После запуска приложения, документация будет доступна по стандартному адресу FastAPI:
     - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
     - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

### Запуск с использованием Docker

1. **Копирование и настройка переменных окружения**:
   - Скопируйте файл окружения-примера `.env-example` в `.env-non-dev`:
     ```bash
     cp .env-example .env-non-dev
     ```
   - Замените переменные в файле `.env-non-dev` на ваши собственные данные.

2. **Запуск приложения с использованием Docker**:
   - Соберите и запустите Docker-контейнеры:
     ```bash
     docker-compose up --build -d
     ```

3. **Документация**:
   - После запуска приложения, документация будет доступна по стандартному адресу FastAPI:
     - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
     - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

### Дополнительная информация

Это приложение использует PostgreSQL в качестве базы данных и Alembic для миграций базы данных. Убедитесь, что вы правильно настроили переменные окружения для подключения к базе данных и других настроек.

Если у вас возникли проблемы, проверьте логи для получения дополнительной информации или обратитесь к документации FastAPI и Docker для устранения неполадок.

