# Task Service

Simple task management FastAPI service with JWT.

## Installation
0. Create a `.env` file in the root directory of the project:
    ```dotenv
    DATABASE_URL=postgresql://postgres:password@db:5432/taskdb
    SECRET_KEY=your-secret-key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    REFRESH_TOKEN_EXPIRE_DAYS=7
    ```
1. Clone the repository:
    ```bash
    git clone git@github.com:Azeasy/TestWork2654.git
    cd fastapi_project
    ```

After that you can decide to use either docker or local installation

#### Using Docker
1. Start Docker Compose:
    ```bash
    docker-compose up --build
    ```

#### Local Installation
1. Install Poetry (if not already installed):
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```
2. Install dependencies:
    ```bash
    poetry install
    ```
3. Run the application locally:
    ```bash
    poetry run uvicorn app.main:app --reload
    ```

## Usage

- Swagger Documentation: `http://localhost:8000/docs`
- Registration: `POST /auth/register`
- Login: `POST /auth/login`
- Token Refresh: `POST /auth/refresh`
- Create Task: `POST /tasks`
- Update Task: `PUT /tasks/{task_id}`
- Get Task List: `GET /tasks`
- Search Tasks: `GET /tasks/search?q=<query>`

## Migrations

```bash
alembic upgrade head
```

## Testing

```bash
poetry run pytest
```
