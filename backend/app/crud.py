from .models import Dish, AllergenLikelihood
from .schemas import (
    DishCreate,
    AllergenLikelihoodCreate,
)
from sqlalchemy import select
from typing import Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import Literal


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


def get_all_dishes(db: Session) -> list[Dish]:
    """Retrieves all dishes"""
    dish = db.execute(select(Dish))
    return list(dish.scalars().all())


def search_dish(db: Session, query: str) -> list[Dish]:
    dishes = db.execute(select(Dish).where(Dish.name.ilike(f"%{query}%")))
    return list(dishes.scalars().all())


def get_dish(db: Session, dish_id: int) -> Optional[Dish]:
    """Retrieve a dish by its ID."""
    return db.get(Dish, dish_id)


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
) -> AllergenLikelihood | Literal["dish_not_found"] | Literal["already_exists"]:
    """Create a new allergen likelihood for a dish."""

    dish = db.get(Dish, allergen.dish_id)
    if not dish:
        return "dish_not_found"

    result = db.execute(
        select(AllergenLikelihood).where(
            (AllergenLikelihood.dish_id == allergen.dish_id)
            & (AllergenLikelihood.allergen == allergen.allergen)
        )
    )
    if result.scalar_one_or_none():
        return "already_exists"

    new_entry = AllergenLikelihood(
        dish_id=allergen.dish_id,
        allergen=allergen.allergen,
        likelihood=allergen.likelihood,
    )
    db.add(new_entry)
    try:
        db.commit()
        db.refresh(new_entry)
    except IntegrityError:
        db.rollback()
        return "already_exists"

    return new_entry


def get_all_allergen_likelihood(db: Session) -> list[AllergenLikelihood]:
    allergens = db.execute(select(AllergenLikelihood))
    return list(allergens.scalars().all())


def get_allergen_likelihood(
    db: Session, allergen_id: int
) -> Optional[AllergenLikelihood]:
    """Retrieve a specific allergen likelihood by its ID."""
    return db.get(AllergenLikelihood, allergen_id)


def delete_allergen_likelihood(db: Session, allergen_id: int) -> bool:
    """Delete a specific allergen likelihood instance by ID."""
    result = db.get(AllergenLikelihood, allergen_id)
    if not result:
        return False
    db.delete(result)
    db.commit()
    return True
