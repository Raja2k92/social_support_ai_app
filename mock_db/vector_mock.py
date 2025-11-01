def vector_mock(vectors: list, top_k: int = 2):
    """Simulate vector search returning top_k items."""
    print(f"[VectorMock] Searching top {top_k} of {len(vectors)} vectors")
    return vectors[:top_k]
