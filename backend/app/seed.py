"""Seed script to populate the database with sample data."""

import asyncio
import random

from sqlalchemy import text

from app.core.database import async_session, engine
from app.models import Base, Product, Review, User


SAMPLE_USERS = [
    {"name": "John Doe", "email": "john@example.com"},
    {"name": "Jane Smith", "email": "jane@example.com"},
    {"name": "Bob Wilson", "email": "bob@example.com"},
    {"name": "Alice Brown", "email": "alice@example.com"},
    {"name": "Charlie Davis", "email": "charlie@example.com"},
    {"name": "Diana Lee", "email": "diana@example.com"},
    {"name": "Ethan Park", "email": "ethan@example.com"},
    {"name": "Fiona Chen", "email": "fiona@example.com"},
    {"name": "George Kim", "email": "george@example.com"},
    {"name": "Hannah Liu", "email": "hannah@example.com"},
]

SAMPLE_PRODUCTS = [
    {
        "title": "Gaming Laptop",
        "description": "High-performance gaming laptop with RTX 4080, 32GB RAM, and 1TB SSD. Perfect for AAA gaming and content creation.",
        "image_url": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=800",
    },
    {
        "title": "Wireless Headphones",
        "description": "Premium noise-cancelling wireless headphones with 30-hour battery life and studio-quality sound.",
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800",
    },
    {
        "title": "Mechanical Keyboard",
        "description": "RGB mechanical keyboard with Cherry MX switches, aluminum frame, and programmable keys.",
        "image_url": "https://images.unsplash.com/photo-1541140532154-b024d1b22b6f?w=800",
    },
    {
        "title": "4K Monitor",
        "description": "27-inch 4K IPS monitor with HDR support, 144Hz refresh rate, and USB-C connectivity.",
        "image_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800",
    },
    {
        "title": "Smartphone Stand",
        "description": "Adjustable aluminum smartphone stand with anti-slip base and cable management.",
        "image_url": "https://images.unsplash.com/photo-1586953208270-767889fa9b0e?w=800",
    },
    {
        "title": "USB-C Hub",
        "description": "7-in-1 USB-C hub with HDMI, USB 3.0, SD card reader, and 100W power delivery.",
        "image_url": "https://images.unsplash.com/photo-1625842268584-8f3296236761?w=800",
    },
    {
        "title": "Ergonomic Mouse",
        "description": "Vertical ergonomic wireless mouse with adjustable DPI, silent clicks, and rechargeable battery.",
        "image_url": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=800",
    },
    {
        "title": "Portable SSD 2TB",
        "description": "Ultra-fast portable SSD with 2TB capacity, USB 3.2 Gen 2, and shock-resistant aluminum casing.",
        "image_url": "https://images.unsplash.com/photo-1597848212624-a19eb35e2651?w=800",
    },
    {
        "title": "Webcam 4K",
        "description": "4K ultra HD webcam with autofocus, dual stereo microphones, and low-light correction for streaming.",
        "image_url": "https://images.unsplash.com/photo-1611532736597-de2d4265fba3?w=800",
    },
    {
        "title": "Desk Lamp LED",
        "description": "Adjustable LED desk lamp with 5 color temperatures, USB charging port, and touch controls.",
        "image_url": "https://images.unsplash.com/photo-1507473885765-e6ed057ab6fe?w=800",
    },
    {
        "title": "Bluetooth Speaker",
        "description": "Waterproof Bluetooth speaker with 360-degree sound, 24-hour battery, and built-in microphone.",
        "image_url": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=800",
    },
    {
        "title": "Laptop Backpack",
        "description": "Anti-theft laptop backpack with USB charging port, waterproof fabric, and fits up to 17-inch laptops.",
        "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800",
    },
    {
        "title": "Noise Machine",
        "description": "White noise machine with 30 soothing sounds, timer function, and compact portable design.",
        "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=800",
    },
    {
        "title": "Smart Watch",
        "description": "Fitness smart watch with heart rate monitor, GPS tracking, sleep analysis, and 7-day battery life.",
        "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800",
    },
    {
        "title": "Wireless Charger Pad",
        "description": "15W fast wireless charging pad compatible with all Qi-enabled devices. Slim profile with LED indicator.",
        "image_url": "https://images.unsplash.com/photo-1591290619315-4794e9092528?w=800",
    },
    {
        "title": "Cable Management Kit",
        "description": "Complete cable management solution with clips, sleeves, ties, and adhesive holders for a tidy desk.",
        "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=800",
    },
    {
        "title": "Monitor Light Bar",
        "description": "Screen-mounted LED light bar with adjustable brightness and color temperature. No glare on screen.",
        "image_url": "https://images.unsplash.com/photo-1593062096033-9a26b09da705?w=800",
    },
    {
        "title": "Drawing Tablet",
        "description": "Professional drawing tablet with 8192 pressure levels, tilt support, and customizable express keys.",
        "image_url": "https://images.unsplash.com/photo-1626785774573-4b799315345d?w=800",
    },
    {
        "title": "Microphone USB",
        "description": "Condenser USB microphone with cardioid pattern, gain control, and zero-latency monitoring for podcasts.",
        "image_url": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=800",
    },
    {
        "title": "Keyboard Wrist Rest",
        "description": "Memory foam keyboard wrist rest with cooling gel, non-slip base, and ergonomic design.",
        "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800",
    },
    {
        "title": "Desk Mat XL",
        "description": "Extra-large desk mat with stitched edges, waterproof surface, and non-slip rubber base. 900x400mm.",
        "image_url": "https://images.unsplash.com/photo-1616628188540-925618b4c45a?w=800",
    },
    {
        "title": "Power Strip Tower",
        "description": "Surge-protected power strip tower with 12 outlets, 4 USB ports, and 6ft retractable cord.",
        "image_url": "https://images.unsplash.com/photo-1544281679-e5c0ffc37e80?w=800",
    },
    {
        "title": "Mini Projector",
        "description": "Portable mini projector with 1080p support, built-in speakers, and HDMI/USB connectivity.",
        "image_url": "https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=800",
    },
    {
        "title": "Fingerprint Padlock",
        "description": "Smart fingerprint padlock with 10-fingerprint memory, USB rechargeable, and weather-resistant body.",
        "image_url": "https://images.unsplash.com/photo-1558002038-1055907df827?w=800",
    },
    {
        "title": "Laptop Cooling Pad",
        "description": "Laptop cooling pad with 5 quiet fans, adjustable height, and blue LED lighting. Fits up to 17 inches.",
        "image_url": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=800",
    },
    {
        "title": "Digital Photo Frame",
        "description": "10-inch digital photo frame with IPS display, Wi-Fi, and cloud photo sharing via mobile app.",
        "image_url": "https://images.unsplash.com/photo-1513542789411-b6a5d4f31634?w=800",
    },
    {
        "title": "Desk Organizer",
        "description": "Multi-compartment wooden desk organizer with phone holder, pen slots, and letter tray.",
        "image_url": "https://images.unsplash.com/photo-1544816155-12df9643f363?w=800",
    },
    {
        "title": "Smart Plug 4-Pack",
        "description": "Wi-Fi smart plugs with voice control, scheduling, energy monitoring, and no hub required.",
        "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=800",
    },
    {
        "title": "Ethernet Cable Cat8",
        "description": "50ft Cat8 ethernet cable with gold-plated connectors, 40Gbps speed, and shielded flat design.",
        "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=800",
    },
    {
        "title": "VR Headset",
        "description": "Standalone VR headset with 6DoF tracking, hand tracking, and access to a vast library of VR content.",
        "image_url": "https://images.unsplash.com/photo-1622979135225-d2ba269cf1ac?w=800",
    },
]

SAMPLE_COMMENTS = [
    "Absolutely love it! Exceeded my expectations.",
    "Great quality for the price. Would buy again.",
    "Works exactly as described. Very satisfied.",
    "Solid product, fast shipping too.",
    "Better than I expected. Highly recommend.",
    "Good but could be improved in some areas.",
    "Does the job well. No complaints.",
    "Perfect for my needs. Five stars!",
    "Decent quality. Fair for what you pay.",
    "Not bad, but I've seen better options.",
    "Outstanding build quality and design.",
    "Very practical and well-made.",
    "A must-have for any tech enthusiast.",
    "Impressive performance all around.",
    "Simple, effective, and affordable.",
]


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        result = await session.execute(text("SELECT COUNT(*) FROM products"))
        count = result.scalar()
        if count > 0:
            print(f"Database already has {count} products. Skipping seed.")
            return

        users = [User(**data) for data in SAMPLE_USERS]
        session.add_all(users)
        await session.flush()

        products = [Product(**data) for data in SAMPLE_PRODUCTS]
        session.add_all(products)
        await session.flush()

        random.seed(42)
        review_count = 0
        for product in products:
            num_reviews = random.randint(1, 6)
            reviewers = random.sample(users, num_reviews)
            for user in reviewers:
                review = Review(
                    product_id=product.id,
                    user_id=user.id,
                    rating=random.randint(2, 5),
                    comment=random.choice(SAMPLE_COMMENTS),
                )
                session.add(review)
                review_count += 1

        await session.commit()
        print(f"Seeded {len(users)} users, {len(products)} products, and {review_count} reviews.")


if __name__ == "__main__":
    asyncio.run(seed())