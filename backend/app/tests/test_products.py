import pytest

from app.models import Product, User, Review


@pytest.mark.asyncio
async def test_get_products_empty(client):
    response = await client.get("/api/products")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert data["total"] == 0
    assert data["page"] == 1


@pytest.mark.asyncio
async def test_get_products_with_data(client, db_session):
    product = Product(title="Test Laptop", description="A test laptop", image_url=None)
    db_session.add(product)
    await db_session.flush()

    response = await client.get("/api/products")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert data["page"] == 1
    assert data["total_pages"] >= 1
    item = next(p for p in data["items"] if p["title"] == "Test Laptop")
    assert item["description"] == "A test laptop"
    assert item["average_rating"] is None
    assert item["review_count"] == 0


@pytest.mark.asyncio
async def test_get_products_pagination(client, db_session):
    for i in range(5):
        db_session.add(Product(title=f"Paginated Product {i}", description=f"Desc {i}"))
    await db_session.flush()

    response = await client.get("/api/products?page=1&page_size=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["total"] == 5
    assert data["page_size"] == 2
    assert data["total_pages"] == 3

    response2 = await client.get("/api/products?page=3&page_size=2")
    data2 = response2.json()
    assert len(data2["items"]) == 1


@pytest.mark.asyncio
async def test_get_product_detail(client, db_session):
    user = User(name="Tester", email="tester_detail@test.com")
    product = Product(title="Detail Product", description="With reviews")
    db_session.add_all([user, product])
    await db_session.flush()

    review = Review(product_id=product.id, user_id=user.id, rating=4, comment="Pretty good")
    db_session.add(review)
    await db_session.flush()

    response = await client.get(f"/api/products/{product.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Detail Product"
    assert data["average_rating"] == 4.0
    assert data["review_count"] == 1
    assert len(data["reviews"]) == 1
    assert data["reviews"][0]["user"] == "Tester"
    assert data["reviews"][0]["rating"] == 4


@pytest.mark.asyncio
async def test_get_product_not_found(client):
    response = await client.get("/api/products/99999")
    assert response.status_code == 404