def test_create_and_list_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/search/")
    assert r.status_code == 200

    r = client.get("/notes/search/", params={"q": "Hello"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1


# ---------------------------------------------------------------------------
# Search endpoint – comprehensive tests
# ---------------------------------------------------------------------------


def test_search_case_insensitive(client):
    """Searching for a lowercase term should match an uppercase note title/content."""
    client.post("/notes/", json={"title": "Hello World", "content": "Greeting"})

    r = client.get("/notes/search/", params={"q": "hello"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1, f"Expected at least 1 result, got {len(items)}"
    assert any("Hello" in it["title"] for it in items)


def test_search_partial_match(client):
    """A search term that is a prefix / substring of a word should still match."""
    client.post("/notes/", json={"title": "Hello World", "content": "Greeting"})

    r = client.get("/notes/search/", params={"q": "Hel"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1, f"Expected at least 1 result, got {len(items)}"


def test_search_no_results(client):
    """A search for a term that does not exist in any note returns an empty list."""
    client.post("/notes/", json={"title": "Hello World", "content": "Greeting"})

    r = client.get("/notes/search/", params={"q": "nonexistent"})
    assert r.status_code == 200
    items = r.json()
    assert items == [], f"Expected empty list, got {items}"


def test_search_matches_title(client):
    """The search should match when the query appears in the title."""
    client.post("/notes/", json={"title": "Important", "content": "blah"})

    r = client.get("/notes/search/", params={"q": "Important"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1
    assert any(it["title"] == "Important" for it in items)


def test_search_matches_content(client):
    """The search should match when the query appears only in the content."""
    client.post("/notes/", json={"title": "blah", "content": "Important stuff"})

    r = client.get("/notes/search/", params={"q": "Important"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1
    assert any("Important" in it["content"] for it in items)


def test_search_empty_q_returns_all(client):
    """Passing q='' (empty string) should return every note."""
    client.post("/notes/", json={"title": "Note A", "content": "aaa"})
    client.post("/notes/", json={"title": "Note B", "content": "bbb"})

    r = client.get("/notes/search/", params={"q": ""})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 2, f"Expected at least 2 results, got {len(items)}"


def test_search_no_q_param_returns_all(client):
    """Omitting the q parameter entirely should return every note."""
    client.post("/notes/", json={"title": "Note A", "content": "aaa"})
    client.post("/notes/", json={"title": "Note B", "content": "bbb"})

    r = client.get("/notes/search/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 2, f"Expected at least 2 results, got {len(items)}"


# ---------------------------------------------------------------------------
# PUT / DELETE endpoint tests
# ---------------------------------------------------------------------------


def test_update_note(client):
    """PUT /notes/{id} should update title and content."""
    r = client.post("/notes/", json={"title": "Old", "content": "Old content"})
    note = r.json()

    r = client.put(f"/notes/{note['id']}", json={"title": "New", "content": "New content"})
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "New"
    assert data["content"] == "New content"

    r = client.get(f"/notes/{note['id']}")
    assert r.status_code == 200
    assert r.json()["title"] == "New"


def test_update_nonexistent_note(client):
    """PUT /notes/9999 should return 404."""
    r = client.put("/notes/9999", json={"title": "x", "content": "y"})
    assert r.status_code == 404


def test_delete_note(client):
    """DELETE /notes/{id} should remove the note."""
    r = client.post("/notes/", json={"title": "Doomed", "content": "bye"})
    note = r.json()

    r = client.delete(f"/notes/{note['id']}")
    assert r.status_code == 200
    assert r.json()["detail"] == "Note deleted"

    r = client.get(f"/notes/{note['id']}")
    assert r.status_code == 404


def test_delete_nonexistent_note(client):
    """DELETE /notes/9999 should return 404."""
    r = client.delete("/notes/9999")
    assert r.status_code == 404


# ---------------------------------------------------------------------------
# Validation failure tests (Pydantic Field constraints → 422)
# ---------------------------------------------------------------------------


def test_create_note_empty_title(client):
    """POST /notes/ with empty title should return 422."""
    r = client.post("/notes/", json={"title": "", "content": "hello"})
    assert r.status_code == 422


def test_create_note_empty_content(client):
    """POST /notes/ with empty content should return 422."""
    r = client.post("/notes/", json={"title": "hello", "content": ""})
    assert r.status_code == 422


def test_create_note_missing_fields(client):
    """POST /notes/ with empty body should return 422."""
    r = client.post("/notes/", json={})
    assert r.status_code == 422


def test_update_note_empty_title(client):
    """PUT /notes/{id} with empty title should return 422."""
    r = client.post("/notes/", json={"title": "Valid", "content": "Valid content"})
    assert r.status_code == 201, r.text
    note_id = r.json()["id"]

    r = client.put(f"/notes/{note_id}", json={"title": "", "content": "hello"})
    assert r.status_code == 422
