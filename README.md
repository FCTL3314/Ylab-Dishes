# 📖 Table of contents

[![Python](https://img.shields.io/badge/Python-3.10-3777A7?style=flat-square)](https://www.python.org/)
[![Fastapi](https://img.shields.io/badge/FastAPI-0.100.0-009688?style=flat-square)](https://fastapi.tiangolo.com/)
[![Poetry](https://img.shields.io/badge/Poetry-1.5.1-0992E1?style=flat-square)](https://python-poetry.org/)
[![Pytest](https://img.shields.io/badge/Pytest-Passed-0ca644?style=flat-square)](https://docs.pytest.org/en/7.4.x/)
[![Black](https://img.shields.io/badge/Style-Black-black?style=flat-square)](https://black.readthedocs.io/en/stable/)

<ul>
  <li>
    <b>
      <a href="#-description">Description</a>
    </b>
  </li>
  <li>
    <b>
      <a href="#-peculiarities">Peculiarities</a>
    </b>
  </li>
  <li>
    <b>
      <a href="#-installation">Installation</a>
    </b>
  </li>
  <li>
    <b>
      <a href="#%EF%B8%8F-testing">Testing</a>
    </b>
  </li>
  <li>
    <b>
      <a href="#-pre-commit-hooks">Pre-Commit hooks</a>
    </b>
  </li>
</ul>

# ❗ Исправил:
* **Ошибку при которой удаление записей из Excel файла не отображалось в БД.**
* **GET запрос на получение всех меню со всеми связанными объектами, теперь реализован без использования Celery.**

# 📃 Description

#### Проект для отбора на стажировку от компании Ylab.
#### Использовал:
* Asyncpg для асинхронных запросов к базе данных.
* SQLModel как обёртку поверх SQLAlchemy и Pydantic.
* Alembic для миграций.
* Celery beat для периодических задач.
* Пакетный менеджер Poetry.
#### Выполнил задания повышенной сложности:
* Реализовать вывод количества подменю и блюд для Меню через один (сложный) ORM запрос:
  * **app.menu.repository | line 59**
* Реализовать тестовый сценарий «Проверка кол-ва блюд и подменю в меню» из Postman с помощью pytest:
  * **app.menu.tests.test_routes | line 83**
  * **app.submenu.tests.test_routes | line 94**
* Описать API эндпоинты в соответствий c OpenAPI.
  * **Добавил название, описание и теги для каждого эндпоинта.**
* Реализовать в тестах аналог Django reverse() для FastAPI
  * **Добавил каждому эндпоинту название и затем использовал его в router.url_path_for методе**
* #### Анотация возвращаемых типов для сервисов реализована с помощью Generic и TypeVar, возвращаемый тип сервиса указывается при его создании в модулях dependencies.py.


# ❕ Peculiarities
1. Для прохождения Postman тестов необходимо закоментировать Celery задачу синхронизирующую бд с Excel файлом:
     * **app.celery | line 14**
2. Эндпоинт для получения всех меню со всеми связанными подменю и блюдами:
     * **api/v1/data-processing/all/**
3. Сервисы синхронизации Excel файла с базой данных находятся в следующих дирректориях:
     * **app.data_processing.dependencies.admin**
     * **app.data_processing.services.admin_service**
     * **app.data_processing.services.admin_update_services**


# 💽 Installation

1. #### Clone or download the repository.
2. #### Fill `.env.dist` with the required variables or leave the filled ones for test start and rename the file to `.env`.
3. #### Run docker services: `docker-compose -f docker/local/docker-compose.yml up`.

> Для тестового запуска, переменные из .env.dist менять не нужно, просто переименуйте файл в .env


# ⚒️ Testing

1. #### Complete the first 2 steps of the 💽 Installation section.
2. #### Run docker services for testing: `docker-compose -f docker/local/docker-compose.yml -f docker/test/docker-compose.yml up -d`

> #### Результат выполнения тестов отображается в логах контейнера.
> Контейнер запускается, выполняет тесты и завершает свою работу. Для повторного запуска тестов необходимо перезапустить контейнер.
>
> Для того, что бы не дублировать compose файлы, команда выше использует перезапись. Первый compose файл перезаписываеться вторым.


# 🪝 Pre-Commit hooks

1. #### Install: `pre-commit install`
2. #### Run: `pre-commit run --all-files`
