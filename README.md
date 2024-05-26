# Real Time Chat App

## Overview

This Real-Time Chat Application is built using Django Rest Framework (DRF) for handling RESTful APIs and Django Channels for WebSocket communication, enabling real-time messaging between users.

## Features

- User Authentication: Implements user authentication using Simple JWT.
- Real-Time Messaging: Utilizes WebSocket communication via Django Channels for instant message delivery.

## Project Structure

- `app/` : Contains Django application for user authentication and chat functionality.
  - `services/` : Contains small services for user and chat functionality
  - `tests/` :
    - `test_consumer.py` : Contains test cases for WebSocket consumers
  - `channel_auth_middleware.py` : Custom JWT Auth Middleware for Websocket Authentication
  - `consumers.py` : Defines WebSocket consumer for **Real-Time Messaging**.
  - `models.py` : Defines the models for User, Conversation and Message.
  - `routing.py` : Defines routing configuration for WebSocket connections.
  - `url.py` : Defines URL patterns for RESTful APIs.
  - `views.py` : Defines API views for handling user registration, displaying users and conversations.
- `project/` : Main Project folder - contains settings and configuration files.
  - `settings.py` : Django settings including configuration for Django Rest Framework, Simple JWT, and Django Channels.
  - `asgi.py` : ASGI application entry point for the project, including settings related to Django Channels.

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

### 1. User Registration

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

### 2. Login to your Account

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

### 3. Logout

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

### 4. Display Users List Except Authenticated User

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

### 5. Display Users Chat (Conversation)

Endpoint: `POST /api/users/<uuid:pk>/chat/`

- `pk: recipientId`
  - Example: `497ed80f-66de-45e7-801b-3a29710aa5fb`

Request:

- Method: `GET`
- Headers:
  - `Content-Type: application/json`
  - `Authorization: Bearer {your_access_token}`

Response:

```json
{
  "success": true,
  "msg": "User conversation with messages retrieved successfully.",
  "data": {
    "id": "92660037-7f6e-4934-afd5-218024692005", // conversation_id
    "messages": [
      {
        "text": "Hello admin",
        "sender": {
          "id": "c68872ef-dcfa-470b-a0b6-161d213d1c90",
          "first_name": "john",
          "last_name": "doe"
        },
        "created_at": "2024-05-25T10:31:10.245597Z"
      },
      {
        "text": "Hi john",
        "sender": {
          "id": "497ed80f-66de-45e7-801b-3a29710aa5fb",
          "first_name": "admin",
          "last_name": "admin"
        },
        "created_at": "2024-05-25T10:30:59.838568Z"
      }
    ]
  },
  "status": 200
}
```

### 6. WebSocket Endpoint (Send and receive messages)

Endpoint: `/ws/chat/<str:conversation_id>/?token=<access_token>`

> Example Full Endpoint: `ws://localhost:8000/ws/chat/<str:conversation_id>/?token=<access_token>`

- `conversation_id: Conversation ID between users`
  - Example: `92660037-7f6e-4934-afd5-218024692005`
- `token: {Your access token}`

Request:

- Headers:
  - `Origin: http://127.0.0.1:8000`
- Params:
  - `token: {Your access token}`
- Body:

```json
{
  "message": "Hello",
  "recipient_id": "48dc569e-4ef2-4fef-940e-41a92ebfdcc2"
}
```

Response:

```json
{
  "message": "Hello",
  "recipient_id": "48dc569e-4ef2-4fef-940e-41a92ebfdcc2"
}
```
