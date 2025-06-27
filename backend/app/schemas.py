from pydantic import BaseModel, ConfigDict


class DishBase(BaseModel):
    name: str
    country: str


class AllergenLikelihoodBase(BaseModel):
    dish_id: int
    allergen: str
    likelihood: int


class AllergenLikelihoodRead(AllergenLikelihoodBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class AllergenLikelihoodNested(BaseModel):
    allergen: str
    likelihood: int

    model_config = ConfigDict(from_attributes=True)


class DishRead(DishBase):
    id: int
    allergens: list[AllergenLikelihoodNested] = []

    model_config = ConfigDict(from_attributes=True)
