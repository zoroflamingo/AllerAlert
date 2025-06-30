from app.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class AllergenLikelihood(Base):
    __tablename__ = "allergen_likelihoods"

    id = Column(Integer, primary_key=True, index=True)
    dish_id = Column(Integer, ForeignKey("dishes.id"), nullable=False, index=True)
    allergen = Column(String, nullable=False)
    likelihood = Column(Integer, nullable=False)

    dish = relationship("Dish", back_populates="allergens")
