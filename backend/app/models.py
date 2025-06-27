from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String)

    allergens = relationship(
        "AllergenLikelihood", back_populates="dish", cascade="all, delete-orphan"
    )


class AllergenLikelihood(Base):
    __tablename__ = "allergen_likelihoods"  # plural recommended

    id = Column(Integer, primary_key=True, index=True)
    dish_id = Column(Integer, ForeignKey("dishes.id"), nullable=False, index=True)
    allergen = Column(String, nullable=False)
    likelihood = Column(Integer, nullable=False)

    dish = relationship("Dish", back_populates="allergens")
