# Library Management System

A Flask-based REST API for managing a library system.

## Features

- CRUD operations for books
- Search functionality for books by title or author
- Pagination support
- JWT Authentication
- Automated tests

## How to run the project

1. Clone the repository
2. Create a virtual environment and activate it
3. Install the dependencies using `pip install -r requirements.txt`
4. Run the application using `python app.py`

## Design Choices

- Used Flask for the web framework
- Used SQLAlchemy for ORM
- Used Marshmallow for serialization/deserialization
- Used JWT for authentication

## Assumptions and Limitations

- The database used is SQLite for simplicity
- Only basic authentication is implemented, no refresh tokens present
- Basic Error handling done

## API Endpoints

### Authentication
- POST /api/auth/register - Register a new user
- POST /api/auth/login - Login and get JWT token

### Books
- GET /api/books - Get all books (with pagination and search)
- POST /api/books - Create a new book (requires authentication)
- PUT /api/books/{id} - Update a specific book
- DELETE /api/books/{id} - Delete a specific book

### Users
- GET /api/users - Get all users 
- POST /api/users - Create a new user (requires authentication)
- PUT /api/users/{id} - Update a specific user
- DELETE /api/users/{id} - Delete a specific user



## Future Improvements

1. Can add more diverse and comprehensive  member management functionalities
2. Can implement book borrowing system
3. Can add caching mechanism to store and display frequent results faster
4. Can add more comprehensive error handling