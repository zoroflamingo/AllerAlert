from models import Dish, AllergenLikelihood
from schemas import (
    DishBase,
    DishCreate,
    DishRead,
    AllergenLikelihoodBase,
    AllergenLikelihoodCreate,
    AllergenLikelihoodNested,
    AllergenLikelihoodRead,
)
from sqlalchemy import select
from typing import Union, Optional
from sqlalchemy.exc import IntegrityError


def create_dish(db: session, dish: DishCreate) -> bool:
    result = db.execute(select(Dish).where(Dish.name == dish.name))
    existing = result.scalar_one_or_none()
    if existing:
        return False

    new_dish = Dish(name=dish.name, country=dish.country)
    db.add(new_dish)

    try:
        db.commit()
        db.refresh(new_dish)
    except IntegrityError:
        db.rollback()
        return False

    return True


def get_dish(db: session, dish_id: int) -> Optional[Dish]:
    result = db.get(Dish, dish_id)
    if not result:
        return None
    return result


def delete_dish(db: session, dish_id: int) -> bool:
    result = db.get(Dish, dish_id)
    if not result:
        return False
    db.delete(result)
    db.commit()
    return True


def create_allergen_likelihood(db: session, allergen: AllergenLikelihoodCreate) -> bool:
    result = db.execute(
        select(AllergenLikelihood).where(
            (AllergenLikelihood.dish_id == allergen.dish_id)
            & (AllergenLikelihood.allergen == allergen.allergen)
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        return False

    new_allergen_likelihood = AllergenLikelihood(
        dish_id=allergen.dish_id,
        allergen=allergen.allergen,
        likelihood=allergen.likelihood,
    )
    db.add(new_allergen_likelihood)
    try:
        db.commit()
        db.refresh(new_allergen_likelihood)
    except IntegrityError:
        db.rollback()
        return False

    return True


def get_allergen_likelihood(
    db: session, allergen_id: int
) -> Optional[AllergenLikelihood]:
    result = db.get(AllergenLikelihood, allergen_id)
    if not result:
        return None
    return result


def delete_allergen(db: session, allergen_id: int) -> bool:
    result = db.get(AllergenLikelihood, allergen_id)
    if not result:
        return False
    db.delete(result)
    db.commit()
    return True
