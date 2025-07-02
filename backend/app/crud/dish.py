from app.models.dish import Dish
from app.models.allergen import AllergenLikelihood
from app.schemas.dish import DishCreate
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


def get_all_dishes(db: Session) -> list[Dish]:
    """Retrieves all dishes"""
    dish = db.execute(select(Dish))
    return list(dish.scalars().all())


def search_dish(db: Session, query: str) -> list[Dish]:
    """Searches for dishes by a query"""
    dishes = db.execute(select(Dish).where(Dish.name.ilike(f"%{query}%")))
    return list(dishes.scalars().all())


def get_dish_summary(db: Session, dish_id: int) -> Optional[list[AllergenLikelihood]]:
    """Retrieve a list of dish allergens"""
    dish = db.get(Dish, dish_id)
    if dish is None:
        return None
    return dish.allergens


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
