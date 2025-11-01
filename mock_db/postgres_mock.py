def postgres_mock(query: str, params: tuple = ()):
    """Simulate PostgreSQL query execution."""
    print(f"[PostgresMock] Executed: {query} with {params}")
    return {"query": query, "params": params, "status": "OK"}
