from pydantic import BaseModel, ConfigDict
from typing import List
from .allergen import AllergenLikelihoodNested


class DishBase(BaseModel):
    """Base dish schema."""

    name: str
    country: str


class DishCreate(DishBase):
    """Schema for creating a new dish."""

    pass


class DishRead(DishBase):
    """Schema for reading a dish."""

    id: int
    allergens: List[AllergenLikelihoodNested] = []

    model_config = ConfigDict(from_attributes=True)
