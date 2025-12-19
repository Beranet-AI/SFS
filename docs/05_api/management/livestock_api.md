# Livestock API

Base Path: `/api/v1/livestock/`

---

## GET /livestock/
Returns a list of registered livestock.

**Response**
```json
[
  {
    "id": "cow-42",
    "tag": "A-42",
    "location": {
      "farm_id": "farm-1",
      "barn": "barn-a",
      "zone": "zone-3"
    }
  }
]

POST /livestock/

Registers a new livestock.

Request

{
  "tag": "A-42",
  "location": {
    "farm_id": "farm-1",
    "barn": "barn-a",
    "zone": "zone-3"
  }
}

GET /livestock/{id}/

Returns livestock details

Mapping

Aggregate: Livestock
DTO: livestock.dto
Tests: test_livestock_api.py