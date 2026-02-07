# API Endpoints Summary

## Overview
This API has **21 endpoints** total, with **10 POST endpoints** that accept body schemas. Several endpoints feature **nested body schemas** to showcase PreMan's schema extraction capabilities.

---

## Endpoints with Body Schemas

### 1. **POST /users** - Create User
**Body Schema:** `UserCreate`
```json
{
  "name": "string (1-100 chars)",
  "email": "string (email pattern)",
  "age": "integer (0-150, optional)"
}
```
**Response:** `User` (201 Created)

---

### 2. **PUT /users/{user_id}** - Update User
**Body Schema:** `UserUpdate`
```json
{
  "name": "string (1-100 chars, optional)",
  "email": "string (email pattern, optional)",
  "age": "integer (0-150, optional)"
}
```
**Response:** `User` (200 OK)

---

### 3. **POST /products** - Create Product
**Body Schema:** `ProductCreate`
```json
{
  "name": "string (min 1 char)",
  "price": "float (> 0)",
  "description": "string (optional)",
  "in_stock": "boolean (default: true)"
}
```
**Response:** `Product` (201 Created)

---

### 4. **POST /orders** - Create Order ⭐ **NESTED SCHEMA**
**Body Schema:** `OrderCreate` (nested structure)
```json
{
  "user_id": "integer (> 0)",
  "items": [
    {
      "product_id": "integer (> 0)",
      "quantity": "integer (1-100)",
      "special_instructions": "string (max 500 chars, optional)"
    }
  ],
  "shipping_address": {
    "street": "string (1-200 chars)",
    "city": "string (1-100 chars)",
    "state": "string (2 chars)",
    "zip_code": "string (zip pattern)",
    "country": "string (default: USA)",
    "is_primary": "boolean (default: false)"
  },
  "notes": "string (max 1000 chars, optional)",
  "payment_method": "string (max 50 chars, optional)"
}
```
**Nested Models:**
- `OrderItem` (list of items)
- `AddressCreate` (shipping address)
**Response:** `OrderResponse` (201 Created)

---

### 5. **POST /cart** - Create Shopping Cart ⭐ **NESTED SCHEMA**
**Body Schema:** `CartCreate` (nested structure)
```json
{
  "items": [
    {
      "product_id": "integer (> 0)",
      "quantity": "integer (1-100)"
    }
  ],
  "coupon_code": "string (max 20 chars, optional)"
}
```
**Nested Models:**
- `CartItem` (list of cart items)
**Response:** `Cart` (201 Created)

---

### 6. **POST /auth/login** - Login
**Body Schema:** `LoginRequest`
```json
{
  "email": "string (email pattern)",
  "password": "string (8-100 chars)"
}
```
**Response:** Token object (200 OK)

---

### 7. **POST /auth/register** - Register User
**Body Schema:** `RegisterRequest`
```json
{
  "name": "string (1-100 chars)",
  "email": "string (email pattern)",
  "password": "string (8-100 chars)",
  "confirm_password": "string (8-100 chars)",
  "age": "integer (0-150, optional)"
}
```
**Response:** `User` (201 Created)

---

### 8. **POST /users/{user_id}/addresses** - Add Address
**Body Schema:** `AddressCreate`
```json
{
  "street": "string (1-200 chars)",
  "city": "string (1-100 chars)",
  "state": "string (2 chars)",
  "zip_code": "string (zip pattern: 12345 or 12345-6789)",
  "country": "string (default: USA)",
  "is_primary": "boolean (default: false)"
}
```
**Response:** `Address` (201 Created)

---

### 9. **POST /products/{product_id}/reviews** - Create Review
**Body Schema:** `ReviewCreate`
```json
{
  "rating": "integer (1-5)",
  "title": "string (1-200 chars)",
  "comment": "string (10-2000 chars)",
  "verified_purchase": "boolean (default: false)"
}
```
**Response:** `Review` (201 Created)

---

### 10. **POST /users/{user_id}/notifications/preferences** - Update Preferences ⭐ **ENUM SCHEMA**
**Body Schema:** `NotificationPreferences` (with enum types)
```json
{
  "order_updates": "enum (email|sms|push|none, default: email)",
  "promotions": "enum (email|sms|push|none, default: email)",
  "shipping_updates": "enum (email|sms|push|none, default: sms)",
  "marketing": "enum (email|sms|push|none, default: none)"
}
```
**Nested Features:**
- Enum types (`NotificationType`)
**Response:** Preferences object (200 OK)

---

## GET Endpoints (No Body)

### 11. **GET /** - API Information
**Response:** API info object

### 12. **GET /health** - Health Check
**Response:** Health status object

### 13. **GET /users** - List Users
**Query Params:** `skip`, `limit`, `search`
**Response:** `List[User]`

### 14. **GET /users/{user_id}** - Get User
**Response:** `User`

### 15. **GET /products** - List Products
**Query Params:** `skip`, `limit`, `min_price`, `max_price`, `in_stock`
**Response:** `List[Product]`

### 16. **GET /products/{product_id}** - Get Product
**Response:** `Product`

### 17. **DELETE /users/{user_id}** - Delete User
**Response:** 204 No Content

---

## Nested Schema Highlights

### ⭐ Most Complex Nested Schemas:

1. **POST /orders** - Triple nesting:
   - `OrderCreate` → `List[OrderItem]` → nested `AddressCreate`
   - Multiple validation rules
   - Optional nested objects

2. **POST /cart** - List nesting:
   - `CartCreate` → `List[CartItem]`
   - Array validation (min_items, max_items)

3. **POST /users/{user_id}/notifications/preferences** - Enum nesting:
   - `NotificationPreferences` → multiple `NotificationType` enums
   - Default values for each field

---

## Testability

All endpoints are **fully testable**:

✅ **Body Validation**: All POST/PUT endpoints use Pydantic models with validation
✅ **Nested Structures**: Complex nested schemas properly defined
✅ **Response Models**: All endpoints have `response_model` for schema validation
✅ **Error Handling**: Proper HTTPException handling for 404, 400, 401 errors
✅ **Status Codes**: Correct status codes (200, 201, 204, 400, 401, 404)

---

## Example Test Requests

### Test Order Creation (Nested Schema):
```bash
curl -X POST http://localhost:8000/orders \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "items": [
      {"product_id": 1, "quantity": 2, "special_instructions": "Handle with care"},
      {"product_id": 2, "quantity": 1}
    ],
    "shipping_address": {
      "street": "123 Main St",
      "city": "San Francisco",
      "state": "CA",
      "zip_code": "94102",
      "country": "USA",
      "is_primary": true
    },
    "notes": "Rush delivery",
    "payment_method": "credit_card"
  }'
```

### Test Cart Creation (Nested Schema):
```bash
curl -X POST http://localhost:8000/cart \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {"product_id": 1, "quantity": 3},
      {"product_id": 2, "quantity": 1}
    ],
    "coupon_code": "SAVE10"
  }'
```

### Test Notification Preferences (Enum Schema):
```bash
curl -X POST http://localhost:8000/users/1/notifications/preferences \
  -H "Content-Type: application/json" \
  -d '{
    "order_updates": "sms",
    "promotions": "email",
    "shipping_updates": "push",
    "marketing": "none"
  }'
```

---

## Summary

- **Total Endpoints**: 21
- **POST Endpoints with Body Schemas**: 10
- **Endpoints with Nested Schemas**: 3 (orders, cart, notifications)
- **Endpoints with Enum Types**: 1 (notifications)
- **All endpoints are testable** ✅
