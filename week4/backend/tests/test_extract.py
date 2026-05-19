from backend.app.services.extract import extract_action_items, extract_tags


def test_extract_action_items():
    text = """
    This is a note
    - TODO: write tests
    - Ship it!
    Not actionable
    """.strip()
    items = extract_action_items(text)
    assert "TODO: write tests" in items
    assert "Ship it!" in items


# ---------------------------------------------------------------------------
# Tag extraction tests
# ---------------------------------------------------------------------------


def test_extract_tags_basic():
    text = "Hello #world this is #python"
    tags = extract_tags(text)
    assert tags == ["world", "python"]


def test_extract_tags_with_underscore():
    text = "Use #my_tag and #another_one"
    tags = extract_tags(text)
    assert tags == ["my_tag", "another_one"]


def test_extract_tags_no_match_without_boundary():
    text = "not#tag should not match"
    tags = extract_tags(text)
    assert tags == []


def test_extract_tags_at_start_of_string():
    text = "#start here"
    tags = extract_tags(text)
    assert tags == ["start"]


def test_extract_tags_deduplication():
    text = "#hello world #hello again #hello"
    tags = extract_tags(text)
    assert tags == ["hello"]


def test_extract_tags_empty_string():
    tags = extract_tags("")
    assert tags == []


def test_extract_tags_no_tags():
    text = "This has no tags at all"
    tags = extract_tags(text)
    assert tags == []
