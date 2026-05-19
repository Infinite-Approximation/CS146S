def test_create_and_complete_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 1


def test_complete_nonexistent_item(client):
    """Completing a non-existent item should return 404."""
    r = client.put("/action-items/9999/complete")
    assert r.status_code == 404


def test_complete_already_completed_item(client):
    """Completing an already-completed item is idempotent -- still 200 and completed."""
    r = client.post("/action-items/", json={"description": "Already done"})
    assert r.status_code == 201, r.text
    item = r.json()

    # First completion
    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    assert r.json()["completed"] is True

    # Second completion (idempotent)
    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    assert r.json()["completed"] is True


def test_multiple_items_partial_completion(client):
    """Create 3 items, complete 1 -- list should show 1 done and 2 open."""
    ids = []
    for desc in ["Task A", "Task B", "Task C"]:
        r = client.post("/action-items/", json={"description": desc})
        assert r.status_code == 201, r.text
        ids.append(r.json()["id"])

    # Complete only the first item
    r = client.put(f"/action-items/{ids[0]}/complete")
    assert r.status_code == 200

    r = client.get("/action-items/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 3

    completed = [i for i in items if i["completed"]]
    open_items = [i for i in items if not i["completed"]]
    assert len(completed) == 1, f"Expected 1 completed, got {len(completed)}"
    assert len(open_items) == 2, f"Expected 2 open, got {len(open_items)}"


def test_create_item_starts_uncompleted(client):
    """A newly created action item must have completed == False."""
    r = client.post("/action-items/", json={"description": "Fresh item"})
    assert r.status_code == 201, r.text
    item = r.json()
    assert "id" in item
    assert item["completed"] is False
    assert item["description"] == "Fresh item"


# ---------------------------------------------------------------------------
# Validation failure tests (Pydantic Field constraints → 422)
# ---------------------------------------------------------------------------


def test_create_action_item_empty_description(client):
    """POST /action-items/ with empty description should return 422."""
    r = client.post("/action-items/", json={"description": ""})
    assert r.status_code == 422


def test_create_action_item_missing_description(client):
    """POST /action-items/ with missing description should return 422."""
    r = client.post("/action-items/", json={})
    assert r.status_code == 422
