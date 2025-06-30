from app.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    country = Column(String)

    allergens = relationship(
        "AllergenLikelihood", back_populates="dish", cascade="all, delete-orphan"
    )
