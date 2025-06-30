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
    search_dish,
    get_all_dishes,
    get_all_allergen_likelihood,
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
    new_dish = create_dish(db, dish)
    if not new_dish:
        raise HTTPException(status_code=400, detail="Dish already exists")
    return new_dish


@dishes_router.get(
    "/",
    response_model=list[DishRead],
    summary="Get all dishes",
    description="Retrieves all dishes",
)
def get_all_dishes_endpoint(db: Session = Depends(get_db)) -> list[DishRead]:
    dishes = get_all_dishes(db)
    return [DishRead.model_validate(dish) for dish in dishes]


@dishes_router.get(
    "/search",
    response_model=list[DishRead],
    summary="Searches for dishes",
    description="Searches for dishes by a query",
)
def search_dish_endpoint(query: str, db: Session = Depends(get_db)) -> list[DishRead]:
    dishes = search_dish(db, query)
    return [DishRead.model_validate(dish) for dish in dishes]


@dishes_router.get(
    "/{dish_id}",
    response_model=DishRead,
    summary="Get a dish",
    description="Retrieves a dish by its ID.",
)
def get_dish_endpoint(dish_id: int, db: Session = Depends(get_db)) -> DishRead:
    """Endpoint to retrieve a dish by ID. Returns 404 if not found."""
    dish = get_dish(db, dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    return dish


@dishes_router.delete(
    "/{dish_id}",
    status_code=204,
    summary="Delete a dish",
    description="Deletes a dish by its ID.",
)
def delete_dish_endpoint(dish_id: int, db: Session = Depends(get_db)) -> Response:
    """Endpoint to delete a dish by ID. Returns 204 or 404."""
    response = delete_dish(db, dish_id)
    if not response:
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
    new_allergen = create_allergen_likelihood(db, allergen)
    if new_allergen == "dish_not_found":
        raise HTTPException(status_code=400, detail="Dish does not exist")
    elif new_allergen == "already_exists":
        raise HTTPException(
            status_code=400, detail="Allergen already exists for this dish"
        )
    return new_allergen


@allergens_router.get(
    "/",
    response_model=list[AllergenLikelihoodRead],
    summary="Get all allergen likelihood instances",
    description="Retrieves all allergen likelihood instances",
)
def get_all_allergen_likelihood_endpoint(
    db: Session = Depends(get_db),
) -> list[AllergenLikelihoodRead]:
    allergens_likelihoods = get_all_allergen_likelihood(db)
    return [
        AllergenLikelihoodRead.model_validate(entry) for entry in allergens_likelihoods
    ]


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
    allergen = get_allergen_likelihood(db, allergen_id)
    if not allergen:
        raise HTTPException(status_code=404, detail="Allergen not found")
    return allergen


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
    response = delete_allergen_likelihood(db, allergen_id)
    if not response:
        raise HTTPException(status_code=404, detail="Allergen not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
