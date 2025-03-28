from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    nick_name: Mapped[str] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean(), nullable=False, default=True)

    favorite_planets = relationship(
        "FavoritePlanet", back_populates="user", cascade="all, delete-orphan")
    favorite_characters = relationship(
        "FavoriteCharacter", back_populates="user", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "nick_name": self.nick_name,
            "email": self.email
        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    location: Mapped[str] = mapped_column(String(100), nullable=True)
    main_image: Mapped[str] = mapped_column(
        String, nullable=True)  # URL de la imagen

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "location": self.location,
            "main_image": self.main_image
        }


class Character(db.Model):
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=True)
    likes: Mapped[int] = mapped_column(Integer, default=0)
    homeworld_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("planet.id"), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "text": self.text,
            "likes": self.likes,
            "homeworld_id": self.homeworld_id
        }


class FavoritePlanet(db.Model):
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("planet.id"), nullable=False)

    user = relationship("User", back_populates="favorite_planets")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }


class FavoriteCharacter(db.Model):
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id"), nullable=False)
    character_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("character.id"), nullable=False)

    user = relationship("User", back_populates="favorite_characters")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id
        }
