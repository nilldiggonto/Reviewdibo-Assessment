import pytest

from app.models import Product, User


@pytest.mark.asyncio
async def test_create_review(client, db_session):
    user = User(name="Reviewer", email="reviewer_create@test.com")
    product = Product(title="Review Target", description="A product to review")
    db_session.add_all([user, product])
    await db_session.flush()

    response = await client.post("/api/reviews", json={
        "product_id": product.id,
        "user_id": user.id,
        "rating": 5,
        "comment": "Outstanding product!",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["rating"] == 5
    assert data["comment"] == "Outstanding product!"
    assert data["user"] == "Reviewer"


@pytest.mark.asyncio
async def test_create_review_invalid_rating(client, db_session):
    user = User(name="Bad Reviewer", email="bad_reviewer@test.com")
    product = Product(title="Another Product", description="Test")
    db_session.add_all([user, product])
    await db_session.flush()

    response = await client.post("/api/reviews", json={
        "product_id": product.id,
        "user_id": user.id,
        "rating": 6,
        "comment": "Too high rating",
    })
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_review_product_not_found(client, db_session):
    user = User(name="Lost Reviewer", email="lost_reviewer@test.com")
    db_session.add(user)
    await db_session.flush()

    response = await client.post("/api/reviews", json={
        "product_id": 99999,
        "user_id": user.id,
        "rating": 3,
        "comment": "Product does not exist",
    })
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_review(client, db_session):
    user = User(name="Updater", email="updater@test.com")
    product = Product(title="Update Target", description="To be reviewed then updated")
    db_session.add_all([user, product])
    await db_session.flush()

    create_resp = await client.post("/api/reviews", json={
        "product_id": product.id,
        "user_id": user.id,
        "rating": 3,
        "comment": "Okay",
    })
    review_id = create_resp.json()["id"]

    response = await client.put(f"/api/reviews/{review_id}", json={
        "rating": 5,
        "comment": "Actually great!",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["rating"] == 5
    assert data["comment"] == "Actually great!"


@pytest.mark.asyncio
async def test_delete_review(client, db_session):
    user = User(name="Deleter", email="deleter@test.com")
    product = Product(title="Delete Target", description="To be reviewed then deleted")
    db_session.add_all([user, product])
    await db_session.flush()

    create_resp = await client.post("/api/reviews", json={
        "product_id": product.id,
        "user_id": user.id,
        "rating": 1,
        "comment": "Will delete",
    })
    review_id = create_resp.json()["id"]

    response = await client.delete(f"/api/reviews/{review_id}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_review_not_found(client):
    response = await client.delete("/api/reviews/99999")
    assert response.status_code == 404