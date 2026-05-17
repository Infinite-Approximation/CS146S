import os
import pytest

from ..app.services.extract import extract_action_items, extract_action_items_llm


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


def test_extract_action_items_llm_empty():
    """Test that empty input correctly returns an empty list."""
    items = extract_action_items_llm("")
    assert items == []

    items_spaces = extract_action_items_llm("   \n  ")
    assert items_spaces == []


def test_extract_action_items_llm_bullets():
    """Test that bulleted lists and checkboxes are correctly extracted."""
    text = """
    Here are the tasks:
    - [ ] Set up the repo
    * Write documentation
    - Contact the client
    """
    items = extract_action_items_llm(text)

    # Check that it extracted the core tasks (LLMs may rephrase slightly or strip the prefix, so we check for key terms)
    combined = " ".join(items).lower()
    assert "repo" in combined
    assert "documentation" in combined
    assert "client" in combined


def test_extract_action_items_llm_keywords():
    """Test that keywords (TODO:, action:, next:) line items are correctly extracted."""
    text = """
    Meeting ended. 
    TODO: deploy to staging
    action: email the team
    next: order lunch
    """
    items = extract_action_items_llm(text)
    combined = " ".join(items).lower()
    assert "staging" in combined
    assert "email" in combined
    assert "lunch" in combined
