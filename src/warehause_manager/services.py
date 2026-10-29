from sqlalchemy.orm import Session
from sqlalchemy import select
from warehause_manager.models import Product
from warehause_manager.schemas import ProductCreate, ProductUpdate, ProductStock


def create_product(db: Session, data: ProductCreate):
    product_data = data.model_dump()
    product = Product(**product_data)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def change_stock(db: Session, data: ProductStock, product_id: int):
    product = get_product_by_id(db, product_id)
    if not product:
        return None

    if product.quantity + data.change < 0:
        return False
    product.quantity += data.change

    db.commit()
    db.refresh(product)
    return product


def get_products(db: Session):
    return db.scalars(select(Product)).all()


def get_product_by_id(db: Session, product_id: int):
    return db.get(Product, product_id)


def update_product(db: Session, product_id: int, data: ProductUpdate):
    product = get_product_by_id(db, product_id)
    if not product:
        return None

    product_data = data.model_dump(exclude_unset=True)
    for key, value in product_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int):
    product = get_product_by_id(db, product_id)
    if not product:
        return False

    db.delete(product)
    db.commit()
    return True
