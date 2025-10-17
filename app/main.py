from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional, List

from . import crud, models, schemas
from .database import get_db, create_tables

create_tables()

app = FastAPI(
    title = 'VNE Techwear API',
    description = 'Backend API for VNE techwear online story',
    version = '1.0.0'
)


@app.get('/')
async def root():
    return {
        'message': 'VNE Techwear API',
        'version': '1.0.0',
        'docs': '/docs'
    }

@app.get(
    '/products',
    response_model = List[schemas.ProductResponse],
    summary = 'Get products',
    description = 'Retire list of products with optional filtering'
)

def read_products(
        skip: int = Query(0, ge = 0, description = 'Number of records to skip'),
        limit: int = Query(100, ge = 1, le = 1000, description = 'Maximum records to return'),
        category: Optional[str] = Query(None, description = 'Filter by category'),
        search: Optional[str] = Query(None, description='Search in product names'),
        db: Session = Depends(get_db)
):
    products = crud.get_products(
        db = db,
        skip = skip,
        limit = limit,
        category = category,
        search = search
    )
    return products

@app.post(
    '/products',
    response_model = schemas.ProductResponse,
    status_code = status.HTTP_201_CREATED,
    summary = 'Create new product'
)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):

    try:
        return crud.create_product(db=db, product=product)
    except ValueError as e:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = str(e)
        )


@app.put(
    '/products/{product_id}',
    response_model = schemas.ProductResponse,
    summary = 'Update product'
)
def update_product(
    product_id: int,
    product_update: schemas.ProductUpdate,
    db: Session = Depends(get_db)
):

    updated_product = crud.update_product(
        db = db,
        product_id = product_id,
        product_update = product_update
    )
    if not updated_product:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= 'Product not found'
        )
    return updated_product


@app.delete(
     '/products/{product_id}',
    status_code = status.HTTP_204_NO_CONTENT,
    summary = 'Delete product'
)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    if not crud.delete_product(db=db, product_id = product_id):
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= 'Product not found'
        )


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)