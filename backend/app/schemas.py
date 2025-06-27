from pydantic import BaseModel, ConfigDict
from typing import List


class DishBase(BaseModel):
    """Base dish schema."""

    name: str
    country: str


class DishCreate(DishBase):
    """Schema for creating a new dish."""

    pass


class AllergenLikelihoodBase(BaseModel):
    """Base allergen likelihood schema"""

    dish_id: int
    allergen: str
    likelihood: int


class AllergenLikelihoodCreate(AllergenLikelihoodBase):
    """Schema for creating a new allergen likelihood instance."""

    pass


class AllergenLikelihoodNested(BaseModel):
    """Schema for reading all allergen likelihood instances related to a specific dish."""

    allergen: str
    likelihood: int

    model_config = ConfigDict(from_attributes=True)


class DishRead(DishBase):
    """Schema for reading a dish."""

    id: int
    allergens: List[AllergenLikelihoodNested] = []

    model_config = ConfigDict(from_attributes=True)


class AllergenLikelihoodRead(AllergenLikelihoodBase):
    """Schema for reading an allergen likelihood instance."""

    id: int

    model_config = ConfigDict(from_attributes=True)
