from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from warehause_manager.database import get_db
from warehause_manager.schemas import ProductCreate, ProductRead, ProductUpdate
from warehause_manager.services import (create_product, get_products,
                                        get_product_by_id, update_product,
                                        delete_product)

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_new_product(data: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, data)


@router.get("/", response_model=list[ProductRead])
def read_products(db: Session = Depends(get_db)):
    return get_products(db)


@router.get("/{product_id}", response_model=ProductRead)
def get_by_id(product_id: int, db: Session = Depends(get_db)):
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=ProductRead)
def update_products(product_id: int, data: ProductUpdate, db: Session = Depends(get_db)):
    product = update_product(db, product_id, data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product



@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_products(product_id: int, db: Session = Depends(get_db)):
    success = delete_product(db, product_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return
