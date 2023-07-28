# 📃 Description

#### Проект для отбора на стажировку от компании Ylab.

### О проекте:

* #### Использовал SQLModel как обёртку поверх SQLAlchemy и Pydantic.
* #### Использовал Alembic для миграций.
* #### Схема бд: https://dbdiagram.io/d/64b968bb02bd1c4a5e6d2e53
* #### Нет Docker Volume для бд по причине не надобности, так как для тестов бд должна быть пуста.
* #### В связи с тем, что цена блюда это строка, округление пришлось реализовать следующим образом:
```    
def __init__(self, **kwargs):
    if "price" in kwargs:
        template = f"{{:.{Config.DISH_PRICE_ROUNDING}f}}"
        kwargs["price"] = template.format(float(kwargs["price"]))
    super().__init__(**kwargs)
```


# 💽 Installation

1. #### Clone or download the repository.
2. #### Fill `.env.dist` with the required variables or leave the filled ones for test start and rename the file to `.env`.
3. #### Run docker services: `docker-compose -f docker/local/docker-compose.yml up`.

> Для тестового запуска, переменные из .env.dist менять не нужно, просто переименуйте файл в .env


# 🔍 Testing

1. #### Run docker services for testing: `docker-compose -f docker/local/docker-compose.yml -f docker/test/docker-compose.yml up -d`

> Для того, что бы не дублировать compose файлы, команда выше использует перезапись файлов.