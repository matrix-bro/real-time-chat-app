# Real Time Chat App

This is a Real Time Chat Application created using Django Rest Framework.

## Run this project locally

1. Clone the repository:

```bash
git clone https://github.com/matrix-bro/real-time-chat-app.git
```

2. Go to project's folder

```bash
cd real-time-chat-app
```

3. Create a virtual environment and activate it

```bash
python -m venv venv

(In windows)
.\venv\Scripts\activate

(In linux)
source venv/bin/activate
```

4. Install dependencies from requirements file

```bash
pip install -r requirements.txt
```

5. Apply migrations

```bash
python manage.py migrate
```

6. Start the development server

```bash
python manage.py runserver
```

## API Documentation

### User Registration API

#### 1. Creates a New User Account

Endpoint: `POST /api/register/`

Request:

- Method: `POST`
- Headers:
  - `Content-Type: application/json`
- Body:

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@gmail.com",
  "password": "password321",
  "confirm_password": "password321"
}
```

Response:

```json
{
  "success": true,
  "msg": "User account created successfully.",
  "data": {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@gmail.com"
  },
  "status": 201
}
```

#### 2. Login to your Account

Endpoint: `POST /api/login/`

Request:

- Method: `POST`
- Headers:
  - `Content-Type: application/json`
- Body:

```json
{
  "email": "john@gmail.com",
  "password": "password321"
}
```

Response:

```json
{
  "refresh": "Refresh token here",
  "access": "Access token here"
}
```

#### 3. Logout

Endpoint: `POST /api/logout/`

Request:

- Method: `POST`
- Headers:
  - `Content-Type: application/json`
  - `Authorization: Bearer {your_access_token}`
- Body:

```json
{
  "refresh": "your refresh token"
}
```

Response:

- Status: 200 OK

```json
{}
```

#### 3. Display Users List Except Authenticated User

Endpoint: `POST /api/users/`

Request:

- Method: `GET`
- Headers:
  - `Content-Type: application/json`
  - `Authorization: Bearer {your_access_token}`

Response:

- Status: 200 OK

```json
[
  {
    "id": "497ed80f-66de-45e7-801b-3a29710aa5fb",
    "first_name": "ray",
    "last_name": "doe"
  },
  {
    "id": "995d8b85-0a69-4656-b682-f99d93b153d7",
    "first_name": "user2",
    "last_name": "doe"
  }
]
```
