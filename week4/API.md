# API Reference

Base URL: `http://127.0.0.1:8000`

All endpoints accept and return `application/json`.

---

## Schemas

### NoteCreate

| Field     | Type  | Constraints              | Description       |
|-----------|-------|--------------------------|-------------------|
| `title`   | str   | required, 1-200 chars    | Note title        |
| `content` | str   | required, min 1 char     | Note body text    |

### NoteRead

| Field     | Type  | Description       |
|-----------|-------|-------------------|
| `id`      | int   | Note ID           |
| `title`   | str   | Note title        |
| `content` | str   | Note body text    |

### NoteUpdate

| Field     | Type  | Constraints              | Description       |
|-----------|-------|--------------------------|-------------------|
| `title`   | str   | required, 1-200 chars    | New note title    |
| `content` | str   | required, min 1 char     | New note content  |

### ActionItemCreate

| Field          | Type  | Constraints          | Description              |
|----------------|-------|----------------------|--------------------------|
| `description`  | str   | required, min 1 char | Action item description  |

### ActionItemRead

| Field          | Type   | Description                   |
|----------------|--------|-------------------------------|
| `id`           | int    | Action item ID                |
| `description`  | str    | Action item description       |
| `completed`    | bool   | Whether the item is completed |

### ExtractResult

| Field          | Type       | Description                        |
|----------------|------------|------------------------------------|
| `action_items` | list[str]  | Extracted action item descriptions |
| `tags`         | list[str]  | Extracted tags (e.g. `#tag`)       |

---

## Notes

### `GET /notes/`

List all notes.

**Response** `200 OK`

```json
[
  {
    "id": 1,
    "title": "My Note",
    "content": "Some content"
  }
]
```

---

### `POST /notes/`

Create a new note.

**Request Body** (`NoteCreate`)

```json
{
  "title": "My Note",
  "content": "Some content"
}
```

**Response** `201 Created`

Returns the created `NoteRead` object.

---

### `GET /notes/search/?q=<query>`

Search notes by title and content (case-insensitive substring match).

| Param | Type | Required | Description         |
|-------|------|----------|---------------------|
| `q`   | str  | No       | Search query string |

If `q` is omitted or empty, all notes are returned.

**Response** `200 OK`

```json
[
  {
    "id": 1,
    "title": "My Note",
    "content": "Some content"
  }
]
```

---

### `GET /notes/{note_id}`

Get a single note by ID.

| Param    | Type | Description |
|----------|------|-------------|
| `note_id`| int  | Note ID     |

**Response** `200 OK`

Returns the `NoteRead` object.

**Error** `404 Not Found` -- note does not exist.

---

### `POST /notes/{note_id}/extract`

Extract action items and tags from a note's content. Created action items are persisted to the database.

| Param    | Type | Description |
|----------|------|-------------|
| `note_id`| int  | Note ID     |

**Response** `200 OK`

```json
{
  "action_items": ["Buy groceries", "Call dentist"],
  "tags": ["shopping", "health"]
}
```

**Error** `404 Not Found` -- note does not exist.

---

### `PUT /notes/{note_id}`

Update a note's title and content.

| Param    | Type | Description |
|----------|------|-------------|
| `note_id`| int  | Note ID     |

**Request Body** (`NoteUpdate`)

```json
{
  "title": "Updated Title",
  "content": "Updated content"
}
```

**Response** `200 OK`

Returns the updated `NoteRead` object.

**Error** `404 Not Found` -- note does not exist.

---

### `DELETE /notes/{note_id}`

Delete a note.

| Param    | Type | Description |
|----------|------|-------------|
| `note_id`| int  | Note ID     |

**Response** `200 OK`

```json
{
  "detail": "Note deleted"
}
```

**Error** `404 Not Found` -- note does not exist.

---

## Action Items

### `GET /action-items/`

List all action items.

**Response** `200 OK`

```json
[
  {
    "id": 1,
    "description": "Buy groceries",
    "completed": false
  }
]
```

---

### `POST /action-items/`

Create a new action item.

**Request Body** (`ActionItemCreate`)

```json
{
  "description": "Buy groceries"
}
```

**Response** `201 Created`

Returns the created `ActionItemRead` object. The `completed` field defaults to `false`.

---

### `PUT /action-items/{item_id}/complete`

Mark an action item as completed.

| Param    | Type | Description      |
|----------|------|------------------|
| `item_id`| int  | Action item ID   |

**Response** `200 OK`

Returns the updated `ActionItemRead` object with `completed: true`.

**Error** `404 Not Found` -- action item does not exist.
