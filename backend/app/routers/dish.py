from fastapi import APIRouter, Depends, HTTPException, Response, status
from app.schemas.dish import (
    DishCreate,
    DishRead,
)
from app.schemas.allergen import AllergenLikelihoodNested
from app.database import get_db
from app.crud.dish import (
    create_dish,
    get_dish,
    delete_dish,
    search_dish,
    get_all_dishes,
    get_dish_summary,
)
from sqlalchemy.orm import Session
from app.constants import dish_not_found

router = APIRouter(prefix="/dishes", tags=["dishes"])


@router.post(
    "/",
    response_model=DishRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a dish",
    description="Create a new dish entry in the database.",
)
def create_dish_endpoint(dish: DishCreate, db: Session = Depends(get_db)) -> DishRead:
    """Endpoint to create a new dish. Returns 400 if it already exists."""
    new_dish = create_dish(db, dish)
    if not new_dish:
        raise HTTPException(status_code=400, detail="Dish already exists")
    return new_dish


@router.get(
    "/",
    response_model=list[DishRead],
    summary="Get all dishes",
    description="Retrieves all dishes",
)
def get_all_dishes_endpoint(db: Session = Depends(get_db)) -> list[DishRead]:
    dishes = get_all_dishes(db)
    return [DishRead.model_validate(dish) for dish in dishes]


@router.get(
    "/search",
    response_model=list[DishRead],
    summary="Searches for dishes",
    description="Searches for dishes by a query",
)
def search_dish_endpoint(query: str, db: Session = Depends(get_db)) -> list[DishRead]:
    dishes = search_dish(db, query)
    return [DishRead.model_validate(dish) for dish in dishes]


@router.get(
    "/summary",
    response_model=list[AllergenLikelihoodNested],
    summary="Get dish summary",
    description="Retrieve a list of dish allergens",
)
def get_dish_summary_endpoint(
    dish_id: int, db: Session = Depends(get_db)
) -> list[AllergenLikelihoodNested]:
    allergens = get_dish_summary(db, dish_id)
    if allergens is None:
        raise HTTPException(status_code=404, detail=dish_not_found)
    return [AllergenLikelihoodNested.model_validate(allergen) for allergen in allergens]


@router.get(
    "/{dish_id}",
    response_model=DishRead,
    summary="Get a dish",
    description="Retrieves a dish by its ID.",
)
def get_dish_endpoint(dish_id: int, db: Session = Depends(get_db)) -> DishRead:
    """Endpoint to retrieve a dish by ID. Returns 404 if not found."""
    dish = get_dish(db, dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail=dish_not_found)
    return dish


@router.delete(
    "/{dish_id}",
    status_code=204,
    summary="Delete a dish",
    description="Deletes a dish by its ID.",
)
def delete_dish_endpoint(dish_id: int, db: Session = Depends(get_db)) -> Response:
    """Endpoint to delete a dish by ID. Returns 204 or 404."""
    response = delete_dish(db, dish_id)
    if not response:
        raise HTTPException(status_code=404, detail=dish_not_found)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
