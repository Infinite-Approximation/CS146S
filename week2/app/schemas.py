from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel


class NoteCreate(BaseModel):
    content: str


class NoteResponse(BaseModel):
    id: int
    content: str
    created_at: str


class ActionItemResponse(BaseModel):
    id: int
    note_id: Optional[int]
    text: str
    done: bool
    created_at: str


class ExtractRequest(BaseModel):
    text: str
    save_note: bool = False


class ExtractResponse(BaseModel):
    note_id: Optional[int]
    items: List[ActionItemResponse]


class MarkDoneRequest(BaseModel):
    done: bool = True


class MarkDoneResponse(BaseModel):
    id: int
    done: bool
