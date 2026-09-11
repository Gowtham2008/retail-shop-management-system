from sqlalchemy.orm import Session
from database.models import Category


def get_all_categories(db: Session):
    return db.query(Category).all()


def create_category(db: Session, category: Category):
    db.add(category)
    db.commit()
    db.refresh(category)
    return category