# POS Purchase API

`POST /api/pos/purchase`

Records a purchase sent from a point-of-sale system. The request body must be JSON with the following fields:

- `store_id` (string): Identifier of the store processing the purchase.
- `user_id` (string): Identifier of the customer.
- `amount` (number): Total amount of the purchase.
- `items` (array): List of purchased items.
- `timestamp` (string): ISO 8601 timestamp when the purchase occurred.

## Request

```json
{
  "store_id": "store1",
  "user_id": "user123",
  "amount": 120.5,
  "items": ["shirt", "shoes"],
  "timestamp": "2024-01-15T14:30:00"
}
```

## Successful Response

Status: `201 Created`

```json
{ "success": true }
```

## Error Response

Status: `400 Bad Request`

```json
{ "error": "user_id is required" }
```
