from .models import Dish, AllergenLikelihood
from .schemas import (
    DishCreate,
    AllergenLikelihoodCreate,
)
from sqlalchemy import select
from typing import Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def create_dish(db: Session, dish: DishCreate) -> Optional[Dish]:
    """Create a new dish if it doesn't already exist."""
    result = db.execute(select(Dish).where(Dish.name == dish.name))
    existing = result.scalar_one_or_none()
    if existing:
        return None

    new_dish = Dish(name=dish.name, country=dish.country)
    db.add(new_dish)

    try:
        db.commit()
        db.refresh(new_dish)
    except IntegrityError:
        db.rollback()
        return None

    return new_dish


def get_dish(db: Session, dish_id: int) -> Optional[Dish]:
    """Retrieve a dish by its ID."""
    result = db.get(Dish, dish_id)
    if not result:
        return None
    return result


def delete_dish(db: Session, dish_id: int) -> bool:
    """Delete a dish by its ID if it exists."""
    result = db.get(Dish, dish_id)
    if not result:
        return False
    db.delete(result)
    db.commit()
    return True


def create_allergen_likelihood(
    db: Session, allergen: AllergenLikelihoodCreate
) -> Optional[AllergenLikelihood]:
    """Create a new allergen likelihood for a dish, if not already present."""
    result = db.execute(
        select(AllergenLikelihood).where(
            (AllergenLikelihood.dish_id == allergen.dish_id)
            & (AllergenLikelihood.allergen == allergen.allergen)
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        return None

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
        return None

    return new_allergen_likelihood


def get_allergen_likelihood(
    db: Session, allergen_id: int
) -> Optional[AllergenLikelihood]:
    """Retrieve a specific allergen likelihood by its ID."""
    result = db.get(AllergenLikelihood, allergen_id)
    if not result:
        return None
    return result


def delete_allergen_likelihood(db: Session, allergen_id: int) -> bool:
    """Delete a specific allergen likelihood instance by ID."""
    result = db.get(AllergenLikelihood, allergen_id)
    if not result:
        return False
    db.delete(result)
    db.commit()
    return True
