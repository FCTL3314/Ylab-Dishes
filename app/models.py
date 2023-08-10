from uuid import UUID, uuid4

from sqlmodel import Field, Relationship

from app.config import Config
from app.dish.schemas import DishBase
from app.menu.schemas import MenuBase
from app.submenu.schemas import SubmenuBase


class Menu(MenuBase, table=True):  # type: ignore
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    submenus: list['Submenu'] = Relationship(
        sa_relationship_kwargs={
            'cascade': 'all,delete,delete-orphan',
            'lazy': 'selectin',
        },
        back_populates='menu',
    )

    @property
    def submenus_list(self):
        return self.submenus


class Submenu(SubmenuBase, table=True):  # type: ignore
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    menu_id: UUID = Field(default=None, foreign_key='menu.id')

    menu: 'Menu' = Relationship(back_populates='submenus')
    dishes: list['Dish'] = Relationship(
        sa_relationship_kwargs={
            'cascade': 'all,delete,delete-orphan',
            'lazy': 'selectin',
        },
        back_populates='submenu',
    )

    @property
    def dishes_list(self):
        return self.dishes


class Dish(DishBase, table=True):
    def __init__(self, **kwargs):
        """Rounds price to dish rounding config setting."""
        if 'price' in kwargs:
            template = f'{{:.{Config.DISH_PRICE_ROUNDING}f}}'
            kwargs['price'] = template.format(float(kwargs['price']))
        super().__init__(**kwargs)

    id: UUID | None = Field(default_factory=uuid4, primary_key=True)  # type: ignore
    submenu_id: UUID | None = Field(default=None, foreign_key='submenu.id')

    submenu: Submenu = Relationship(
        sa_relationship_kwargs={'lazy': 'selectin'},
        back_populates='dishes',
    )
