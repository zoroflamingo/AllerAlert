from fastapi import APIRouter, Depends, HTTPException, Response, status
from .schemas import (
    DishCreate,
    DishRead,
    AllergenLikelihoodCreate,
    AllergenLikelihoodRead,
)
from .database import get_db
from .crud import (
    create_dish,
    get_dish,
    delete_dish,
    create_allergen_likelihood,
    get_allergen_likelihood,
    delete_allergen_likelihood,
)
from sqlalchemy.orm import Session


dishes_router = APIRouter(prefix="/dishes", tags=["dishes"])
allergens_router = APIRouter(prefix="/allergens", tags=["allergens"])


@dishes_router.post(
    "/",
    response_model=DishRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a dish",
    description="Create a new dish entry in the database.",
)
def create_dish_endpoint(dish: DishCreate, db: Session = Depends(get_db)) -> DishRead:
    """Endpoint to create a new dish. Returns 400 if it already exists."""
    result = create_dish(db, dish)
    if not result:
        raise HTTPException(status_code=400, detail="Dish already exists")
    return result


@dishes_router.get(
    "/{dish_id}",
    response_model=DishRead,
    summary="Get a dish",
    description="Retrieves a dish by its ID.",
)
def get_dish_endpoint(dish_id: int, db: Session = Depends(get_db)) -> DishRead:
    """Endpoint to retrieve a dish by ID. Returns 404 if not found."""
    result = get_dish(db, dish_id)
    if not result:
        raise HTTPException(status_code=404, detail="Dish not found")
    return result


@dishes_router.delete(
    "/{dish_id}",
    status_code=204,
    summary="Delete a dish",
    description="Deletes a dish by its ID.",
)
def delete_dish_endpoint(dish_id: int, db: Session = Depends(get_db)) -> Response:
    """Endpoint to delete a dish by ID. Returns 204 or 404."""
    result = delete_dish(db, dish_id)
    if not result:
        raise HTTPException(status_code=404, detail="Dish not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@allergens_router.post(
    "/",
    response_model=AllergenLikelihoodRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create an allergen likelihood entry",
    description="Create a new allergen likelihood entry in the database.",
)
def create_allergen_likelihood_endpoint(
    allergen: AllergenLikelihoodCreate, db: Session = Depends(get_db)
) -> AllergenLikelihoodRead:
    """Endpoint to create a new allergen likelihood entry for a dish. Returns 400 if duplicate."""
    result = create_allergen_likelihood(db, allergen)
    if not result:
        raise HTTPException(
            status_code=400, detail="Allergen likelihood entry already exists"
        )
    return result


@allergens_router.get(
    "/{allergen_id}",
    response_model=AllergenLikelihoodRead,
    summary="Get an allergen likelihood entry",
    description="Retrieves a allergen likelihood entry by its ID",
)
def get_allergen_likelihood_endpoint(
    allergen_id: int, db: Session = Depends(get_db)
) -> AllergenLikelihoodRead:
    """Endpoint to get allergen likelihood entry info by ID. Returns 404 if not found."""
    result = get_allergen_likelihood(db, allergen_id)
    if not result:
        raise HTTPException(status_code=404, detail="Allergen not found")
    return result


@allergens_router.delete(
    "/{allergen_id}",
    status_code=204,
    summary="Deletes an allergen likelihood entry",
    description="deletes an allergen likelihood entry by its ID",
)
def delete_allergen_likelihood_endpoint(
    allergen_id: int, db: Session = Depends(get_db)
) -> Response:
    """Endpoint to delete allergen likelihood entry by ID. Returns 204 or 404."""
    result = delete_allergen_likelihood(db, allergen_id)
    if not result:
        raise HTTPException(status_code=404, detail="Allergen not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
