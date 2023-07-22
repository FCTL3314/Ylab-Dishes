# 📃 Description

#### Проект для отбора на стажировку от компании Ylab.

### О проекте:

* #### Использовал SQLModel как обёртку поверх SQLAlchemy и Pydantic.
* #### Использовал Alembic для миграций.
* #### Схема бд: https://dbdiagram.io/d/64b968bb02bd1c4a5e6d2e53
* #### Нет Docker Volume для бд по причине не надобности, так как для тестов бд должна быть пуста.


# 💽 Installation

1. #### Clone or download the repository.
2. #### Fill `.env.dist` with the required variables or leave the filled ones and rename the file to `.env`.
3. #### Run docker services: `docker-compose -f docker/local/docker-compose.yml up`.

> Для тестового запуска, переменные из .env.dist менять не нужно, просто переименуйте файл в .env
