from __future__ import annotations

from fastapi import APIRouter, HTTPException

from .. import db
from ..schemas import (
    ActionItemResponse,
    ExtractRequest,
    ExtractResponse,
    MarkDoneRequest,
    MarkDoneResponse,
)
from ..services.extract import extract_action_items, extract_action_items_llm

router = APIRouter(prefix="/action-items", tags=["action-items"])


@router.post("/extract", response_model=ExtractResponse)
def extract(payload: ExtractRequest) -> ExtractResponse:
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is required")

    note_id: int | None = None
    if payload.save_note:
        note_id = db.insert_note(text)

    items = extract_action_items(text)
    ids = db.insert_action_items(items, note_id=note_id)

    # We fetch the inserted items back from the DB to get their full schema
    db.list_action_items(note_id=note_id)
    # Note: list_action_items will return all action items for this note_id
    # Since we just created it, it will be the ones we just inserted
    if note_id is None:
        # If no note was created, we fetch the newly inserted items by id
        # Alternatively, we could construct the response directly from the db rows.
        pass

    # A simpler way to return:
    action_items_resp = []
    for r in db.list_action_items():
        if r["id"] in ids:
            action_items_resp.append(
                ActionItemResponse(
                    id=r["id"],
                    note_id=r["note_id"],
                    text=r["text"],
                    done=bool(r["done"]),
                    created_at=r["created_at"],
                )
            )

    return ExtractResponse(note_id=note_id, items=action_items_resp)


@router.post("/extract-llm", response_model=ExtractResponse)
def extract_llm(payload: ExtractRequest) -> ExtractResponse:
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is required")

    note_id: int | None = None
    if payload.save_note:
        note_id = db.insert_note(text)

    # Calling the new LLM-powered extractor
    items = extract_action_items_llm(text)
    ids = db.insert_action_items(items, note_id=note_id)

    action_items_resp = []
    for r in db.list_action_items():
        if r["id"] in ids:
            action_items_resp.append(
                ActionItemResponse(
                    id=r["id"],
                    note_id=r["note_id"],
                    text=r["text"],
                    done=bool(r["done"]),
                    created_at=r["created_at"],
                )
            )

    return ExtractResponse(note_id=note_id, items=action_items_resp)


@router.get("", response_model=list[ActionItemResponse])
def list_all(note_id: int | None = None) -> list[ActionItemResponse]:
    rows = db.list_action_items(note_id=note_id)
    return [
        ActionItemResponse(
            id=r["id"],
            note_id=r["note_id"],
            text=r["text"],
            done=bool(r["done"]),
            created_at=r["created_at"],
        )
        for r in rows
    ]


@router.post("/{action_item_id}/done", response_model=MarkDoneResponse)
def mark_done(action_item_id: int, payload: MarkDoneRequest) -> MarkDoneResponse:
    try:
        db.mark_action_item_done(action_item_id, payload.done)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return MarkDoneResponse(id=action_item_id, done=payload.done)
