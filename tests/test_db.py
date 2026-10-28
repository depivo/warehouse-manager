from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from warehause_manager import database
from warehause_manager.database import get_db
from warehause_manager.schemas import ProductCreate, ProductUpdate
from warehause_manager.services import (
    create_product,
    delete_product,
    get_product_by_id,
    get_products,
    update_product,
)


def test_get_db_yields_session_and_closes(monkeypatch):
    fake_session = MagicMock(spec=Session)
    monkeypatch.setattr(database, "SessionLocal", lambda: fake_session)

    gen = get_db()
    assert next(gen) is fake_session

    gen.close()
    fake_session.close.assert_called_once()


def test_create_product(db):
    data = ProductCreate(name="Заглушка", quantity=10)
    product = create_product(db, data)

    assert product.id == 1
    assert product.name == "Заглушка"
    assert product.quantity == 10


def test_get_products(db):
    create_product(db, ProductCreate(name="Хлеб", quantity=1))
    create_product(db, ProductCreate(name="Молоко", quantity=2))

    products = get_products(db)

    assert len(products) == 2
    assert products[0].name == "Хлеб"


def test_get_products_empty(db):
    assert get_products(db) == []


def test_get_product_by_id_returns_product(db):
    created = create_product(db, ProductCreate(name="Хлеб", quantity=1))

    found = get_product_by_id(db, created.id)

    assert found.name == "Хлеб"


def test_get_product_by_id_missing_returns_none(db):
    assert get_product_by_id(db, 999) is None


def test_update_product_changes_only_passed_fields(db):
    created = create_product(db, ProductCreate(name="Хлеб", quantity=10, comment="свежий"))

    updated = update_product(db, created.id, ProductUpdate(name="Батон"))

    assert updated.name == "Батон"
    assert updated.quantity == 10
    assert updated.comment == "свежий"


def test_update_missing_product_returns_none(db):
    assert update_product(db, 999, ProductUpdate(name="Батон")) is None


def test_delete_product(db):
    created = create_product(db, ProductCreate(name="Хлеб", quantity=1))

    assert delete_product(db, created.id) is True
    assert get_product_by_id(db, created.id) is None


def test_delete_missing_product_returns_false(db):
    assert delete_product(db, 999) is False
