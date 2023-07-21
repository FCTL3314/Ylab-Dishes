from sqlalchemy import Column, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db import Base


class Menu(Base):
    __tablename__ = 'menus'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    submenus = relationship(
        "Submenu", back_populates="menu", cascade="all, delete-orphan"
    )


class Submenu(Base):
    __tablename__ = 'submenus'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    menu_id = Column(Integer, ForeignKey("menus.id"))

    menu = relationship("Menu", back_populates="submenu")
    dishes = relationship("Dish", back_populates="submenu")

    __table_args__ = (UniqueConstraint("name", "menu_id"),)


class Dish(Base):
    __tablename__ = 'dishes'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    submenu_id = Column(Integer, ForeignKey("submenus.id"))

    submenu = relationship("Submenu", back_populates="dish")
