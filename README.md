# LawVriksh Credits Service

A FastAPI-based credit tracking service for LawVriksh platform.

## Features

- User credit management
- REST API endpoints for credit operations
- Automated daily credit allocation
- PostgreSQL database integration
- Background task scheduling

## Quick Setup

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Database Setup**
```bash
# Create PostgreSQL database
createdb CreditManagmentService

# Run schema
psql -d CreditManagmentService -f schema.sql
```

3. **Environment Variables**
```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/credit_db"
```

4. **Run Application**
```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Credits
- `GET /api/credits/{user_id}` - Get credit balance
- `POST /api/credits/{user_id}/add` - Add credits
- `POST /api/credits/{user_id}/deduct` - Deduct credits  
- `PATCH /api/credits/{user_id}/reset` - Reset credits

### Users
- `POST /api/users/` - Create user
- `GET /api/users/{user_id}` - Get user

## Background Tasks

- Daily credit update: Adds 5 credits to all users at midnight UTC

## Testing

Access API documentation at: `http://localhost:8000/docs`

## Database Schema

- `users`: User information
- `credits`: Credit tracking with timestamps