def mongo_mock(collection: str):
    """Simulate MongoDB insert + return collection state."""
    print(f"[MongoMock] Inserted into '{collection}': {collection}")
    return "db"
