from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import Category
from schemas.category import CategoryCreate, CategoryResponse
from repositories.category_repository import (
    get_all_categories,
    create_category
)

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.get("/", response_model=list[CategoryResponse])
def read_categories(db: Session = Depends(get_db)):
    return get_all_categories(db)


@router.post("/", response_model=CategoryResponse, status_code=201)
def add_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    new_category = Category(name=category.name)
    return create_category(db, new_category)