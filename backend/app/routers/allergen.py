from fastapi import APIRouter, Depends, HTTPException, Response, status
from app.schemas.allergen import (
    AllergenLikelihoodCreate,
    AllergenLikelihoodRead,
)
from app.database import get_db
from app.crud.allergen import (
    create_allergen_likelihood,
    get_allergen_likelihood,
    delete_allergen_likelihood,
    get_all_allergen_likelihood,
    get_allergen_likelihoods_by_dish,
)
from sqlalchemy.orm import Session


router = APIRouter(prefix="/allergens", tags=["allergens"])


@router.post(
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
            status_code=400,
            detail="Allergen likelihood entry already exists for this dish",
        )
    return new_allergen


@router.get(
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


@router.get(
    "/by-dish/{dish_id}",
    response_model=list[AllergenLikelihoodRead],
    summary="Get all allergen likelihood instances by dish id",
    description="Retrieves all allergen likelihood instances by dish id",
)
def get_allergen_likelihoods_by_dish_endpoint(
    dish_id: int, db: Session = Depends(get_db)
) -> list[AllergenLikelihoodRead]:
    allergens_likelihoods = get_allergen_likelihoods_by_dish(db, dish_id)
    return [
        AllergenLikelihoodRead.model_validate(entry) for entry in allergens_likelihoods
    ]


@router.get(
    "/id/{allergen_id}",
    response_model=AllergenLikelihoodRead,
    summary="Get an allergen likelihood entry",
    description="Retrieves a allergen likelihood entry by its ID",
)
def get_allergen_likelihood_endpoint(
    allergen_id: int, db: Session = Depends(get_db)
) -> AllergenLikelihoodRead:
    """Endpoint to get allergen likelihood entry info by ID. Returns 404 if not found."""
    allergen = get_allergen_likelihood(db, allergen_id)
    print("Returned allergen from DB:", allergen)
    print("Type:", type(allergen))
    if not allergen:
        raise HTTPException(status_code=404, detail="Allergen not found")
    return allergen


@router.delete(
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
