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
