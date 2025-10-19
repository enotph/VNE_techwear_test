from sqlalchemy.orm import Session
from typing import Optional, List
from . import models, schemas


def get_product(db: Session, product_id: int) -> Optional[models.Product]:                #ищет и возвращает продукт или none

    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_products(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        search: Optional[str] = None
) -> List[models.Product]:

    query = db.query(models.Product)

    if category:
        query = query.filter(models.Product.category.ilike(f'%{category}%'))

    if search:
        query = query.filter(models.Product.name.ilike(f'%{search}%'))

    return query.offset(skip).limit(limit).all()


def create_product(db: Session, product: schemas.ProductCreate) -> models.Product:

    exciting_product = db.query(models.Product).filter(
        models.Product.name == product.name
    ).first()

    if exciting_product:
        raise ValueError(f'Product with name \'{product.name}\' already exists')

    db_product = models.Product(
        name = product.name,
        description = product.description,
        price = product.price,
        category = product.category,
        sizes = ','.join(product.sizes) if product.sizes else None
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(
        db: Session,
        product_id: int,
        product_update: schemas.ProductUpdate
) -> Optional[models.Product]:

    db_product = get_product(db, product_id)
    if not db_product:
        return None

    update_data = product_update.model_dump(exclude_unset=True)

    if 'sizes' in update_data and update_data['sizes'] is not None:
        update_data['sizes'] = ','.join(update_data['sizes'])

    for field, value in update_data.items():
        setattr(db_product, field, value)

    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int) -> bool:

    db_product = get_product(db, product_id)
    if not db_product:
        return False

    db.delete(db_product)
    db.commit()
    return True