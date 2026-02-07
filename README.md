# PreMan Demo Backend

A simple FastAPI backend designed to showcase PreMan's automatic endpoint discovery, schema extraction, and testing capabilities.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

The API will be available at `http://localhost:8000`

## Test with PreMan

```bash
# From Pre-Man-Backend directory
python test_agent_full.py https://github.com/your-username/preman-demo-backend https://forge.api.opentest.live
```

## Endpoints

- `GET /health` - Health check
- `GET /users` - List users (with pagination)
- `GET /users/{user_id}` - Get user by ID
- `POST /users` - Create user
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user
- `POST /users/{user_id}/addresses` - Add user address (nested models)
- `POST /users/{user_id}/notifications/preferences` - Update notification preferences (enums)
- `GET /products` - List products (with filtering)
- `GET /products/{product_id}` - Get product by ID
- `POST /products` - Create product
- `POST /products/{product_id}/reviews` - Create product review (validation constraints)
- `POST /orders` - Create order
- `POST /cart` - Create shopping cart (nested list models)
- `POST /auth/login` - User login (authentication)
- `POST /auth/register` - User registration (password validation)

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🎯 What PreMan Will Discover

When you connect this demo backend, PreMan will automatically:

### 1. Discover All 17 Endpoints

**GET Endpoints:**
- `GET /health` - Health check
- `GET /users` - List users (with pagination and search)
- `GET /users/{user_id}` - Get user by ID
- `GET /products` - List products (with filtering)
- `GET /products/{product_id}` - Get product by ID

**POST Endpoints (9 total - showcasing schema extraction):**
- `POST /users` - Create user (basic model)
- `POST /users/{user_id}/addresses` - Add address (nested models with validation)
- `POST /users/{user_id}/notifications/preferences` - Update preferences (enum types)
- `POST /products` - Create product (price validation)
- `POST /products/{product_id}/reviews` - Create review (rating constraints 1-5)
- `POST /orders` - Create order (query params + body)
- `POST /cart` - Create cart (nested list models)
- `POST /auth/login` - Login (password field)
- `POST /auth/register` - Register (password confirmation)

**Other Endpoints:**
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

### 2. Extract Rich Schemas

PreMan will discover:

**Request Parameters:**
- Query parameters with types and constraints (`skip`, `limit`, `search`)
- Path parameters with validation (`user_id`, `product_id`)
- Request bodies with Pydantic models (`UserCreate`, `ProductCreate`, `AddressCreate`, `ReviewCreate`, `CartCreate`, `LoginRequest`, `RegisterRequest`, `NotificationPreferences`)
- List parameters (`product_ids`, `items` in cart)
- Enum types (`NotificationType`)

**Response Models:**
- Pydantic models (`User`, `Product`, `Address`, `Review`, `Cart`)
- Field types (`str`, `int`, `float`, `bool`, `datetime`, `Enum`)
- Validation rules (`min_length`, `max_length`, `pattern`, `ge`, `le`, `gt`, `min_items`, `max_items`)
- Optional fields
- Nested models (Address, CartItem)
- Default values
- Password fields (with min/max length)

**Status Codes:**
- Success responses (200, 201, 204)
- Error responses (404, 422)

### 3. Generate Tests Automatically

PreMan will create Playwright tests that:
- Test all endpoints with proper request bodies
- Validate response schemas match Pydantic models
- Check status codes
- Test error cases (404, validation errors)
- Test edge cases (empty lists, invalid IDs)

### 4. Run Tests and Show Results

PreMan will execute tests and display:
- ✅ Passing endpoints with status codes and latency
- ❌ Failing endpoints with error details
- ⏱️ Response times for each endpoint
- 📊 Schema validation results

## 📝 Example API Requests

### Create a User
```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30
  }'
```

### List Users
```bash
curl "http://localhost:8000/users?skip=0&limit=10&search=john"
```

### Get User by ID
```bash
curl http://localhost:8000/users/1
```

### Create a Product
```bash
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "price": 999.99,
    "description": "High-performance laptop",
    "in_stock": true
  }'
```

### Create an Order
```bash
curl -X POST "http://localhost:8000/orders?user_id=1&product_ids=1&product_ids=2" \
  -H "Content-Type: application/json" \
  -d '{"notes": "Rush delivery"}'
```

### Add User Address
```bash
curl -X POST http://localhost:8000/users/1/addresses \
  -H "Content-Type: application/json" \
  -d '{
    "street": "123 Main St",
    "city": "San Francisco",
    "state": "CA",
    "zip_code": "94102",
    "country": "USA",
    "is_primary": true
  }'
```

### Create Product Review
```bash
curl -X POST "http://localhost:8000/products/1/reviews?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5,
    "title": "Great product!",
    "comment": "This product exceeded my expectations. Highly recommend!",
    "verified_purchase": true
  }'
```

### Create Shopping Cart
```bash
curl -X POST http://localhost:8000/cart \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {"product_id": 1, "quantity": 2},
      {"product_id": 2, "quantity": 1}
    ],
    "coupon_code": "SAVE10"
  }'
```

### User Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

### User Registration
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "jane@example.com",
    "password": "securepass123",
    "confirm_password": "securepass123",
    "age": 25
  }'
```

### Update Notification Preferences
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

## 🐛 Troubleshooting

### Backend won't start
- **Check port**: Ensure port 8000 is available: `lsof -i :8000`
- **Check dependencies**: Run `pip install -r requirements.txt`
- **Check Python version**: Ensure Python 3.11+ is installed

### PreMan can't connect
- **Verify backend is running**: `curl http://localhost:8000/health`
- **Check base_url**: Include `http://` or `https://` protocol
- **Check network**: Verify connectivity to the base_url
- **Check CORS**: If testing from browser, ensure CORS is configured

### No endpoints discovered
- **Verify FastAPI decorators**: Ensure endpoints use `@app.get()`, `@app.post()`, etc.
- **Check repository**: Verify repository was cloned successfully
- **Check file structure**: Ensure `main.py` is in the root or discoverable location

### Tests failing
- **Check backend logs**: Look for errors in backend console
- **Verify backend is running**: Test endpoints manually with curl
- **Check base_url**: Ensure it points to the correct server
- **Check network**: Verify connectivity between PreMan and backend

## 📚 Next Steps

1. **Customize the Backend**: Add more endpoints, models, or complexity
2. **Add Authentication**: Include auth endpoints to show PreMan's auth handling
3. **Add Database**: Use SQLAlchemy to show PreMan's database model extraction
4. **Add Webhooks**: Include webhook endpoints for more complex scenarios
5. **Deploy**: Deploy to a public URL for easy testing

## 🎯 Success Checklist

Before demoing, ensure:
- ✅ Backend runs locally without errors
- ✅ All 17 endpoints are accessible (including 9 POST endpoints)
- ✅ Swagger UI shows all endpoints with proper schemas
- ✅ Backend is deployed (or accessible via public URL)
- ✅ PreMan can connect and discover endpoints
- ✅ Tests run successfully
- ✅ Schema extraction shows rich metadata (nested models, enums, validation rules)

---

**Ready to demo?** Follow this guide to create your demo backend, then test it with PreMan to see the magic happen! 🚀
