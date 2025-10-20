# ShopTrack Analytics API


A Django REST Framework API for tracking and analyzing shopping cart behavior to reduce e-commerce abandonment rates through data-driven insights and behavioral analytics.

## 🚀 Features

- **User Authentication** - JWT-based secure authentication
- **Product Management** - Full CRUD operations with admin controls
- **Shopping Cart** - Complete cart management with real-time totals
- **Analytics Dashboard** - Behavioral insights and abandonment tracking
- **Admin Interface** - Django admin for data management

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI**: `/swagger/`
- **ReDoc**: `/redoc/`
- **OpenAPI Schema**: `/swagger.json`

### Authentication
All endpoints (except public ones) require JWT authentication.

```bash
# Get access token
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'