# Project Name

A Django-based application with MongoDB Atlas integration.

## Getting Started

### Prerequisites

- Python 3.x
- Virtualenv
- MongoDB Atlas account

### Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/Vipul4439/todo-django-be.git
   cd todo-django-be
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Add your MongoDB Atlas connection string in `.env`:
     ```sh
     DATABASE_URL="your_mongodb_atlas_connection_string"
     ```

### Running the Application

To start the Django app, run:
```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
