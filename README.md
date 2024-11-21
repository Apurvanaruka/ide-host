
# IDE HOST

A web application built with Flask, PostgreSQL, and various integrations including Google and Facebook OAuth for authentication, LangChain for prompt-based interactions, and web scraping functionality.

## Tech Stack

- **Backend**: Python 3.12, Flask
- **Frontend**: HTML, Tailwind CSS
- **Database**: PostgreSQL 16
- **Authentication**: Google OAuth, Facebook OAuth via Flask-Dance
- **Web Scraping**: BeautifulSoup
- **Generative AI**: Google Generative AI (Gemini)
- **Dependencies**:
  - Flask
  - Flask-Dance
  - Flask-SQLAlchemy
  - Flask-Session
  - Flask-Migrate
  - Flask-SQLAlchemy
  - BeautifulSoup
  - dotenv
  - Tailwind CSS

## Setup Instructions

### 1. Create a Virtual Environment
- **Linux/macOS**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

- **Windows**:
  ```bash
  python -m venv venv
  .\venv\Scripts\activate
  ```

### 2. Install Dependencies

Create a `requirements.txt` file with all dependencies listed:
```
Flask
Flask-Dance
Flask-SQLAlchemy
Flask-Session
Flask-Migrate
BeautifulSoup4
google-generativeai
python-dotenv
tailwindcss
```

Then run:
```bash
pip install -r requirements.txt
```

### 3. Initialize the Database
Run the following commands to initialize the PostgreSQL database:

```bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

### 4. Run the Application

To start the Flask app with reloading:
```bash
flask --app run run --reload
```

### 5. Docker Setup
For Docker, create a `Dockerfile` and a `docker-compose.yml` file for easy setup.

#### Dockerfile:
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["flask", "--app", "run", "run", "--reload"]
```

#### docker-compose.yml:
```yaml
version: "3.8"
services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID}
      - GOOGLE_CLIENT_SECRET=${GOOGLE_CLIENT_SECRET}
      - DATABASE_URL=${DATABASE_URL}
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - .:/app
    depends_on:
      - db

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: admin
      POSTGRES_DB: user_db
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Run Docker containers:
```bash
docker-compose up --build
```

## Authentication

- **Google OAuth**: Implemented via Flask-Dance. Use the provided `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` in the `.env` file for authentication.
- **Facebook OAuth**: Implemented via Flask-Dance.

## API Endpoints

- **POST** `/new-prompt`: Create a new prompt.
- **GET, POST, DELETE, PUT** `/prompt`: Manage prompts (CRUD operations).
- **GET, POST, DELETE** `/handle_scrape`: Handle scraped data.
- **POST** `/scrape`: Perform web scraping.

### View API Endpoints

- `@view_bp.route("/")`: Dashboard route.
- `@view_bp.route("/scraperpage")`: Scraping page route.
- `@view_bp.route("/promptpage")`: Prompt page route.

## Environment Variables

Create a `.env` file with the following keys:

```env
GOOGLE_API_KEY=AIzaSyAwIEpg7iGKz-LoYdRBnoF1hycvT5Ks77U
GOOGLE_CLIENT_ID=975512642838-61a9v7bmogtccbdu2b0jqkq8bbq3c0bd.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=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
DATABASE_URL=postgresql://postgres:admin@localhost/user_db
SECRET_KEY=your_secret_key
```

## Features

- **Dashboard**: Displays user profile information (name, email, image), a list of scraped data and prompts.
- **Prompt Page**: Users can view previous prompts, perform CRUD operations, and send new prompts. Responses are generated via Google Gemini.
- **Scraper Page**: Users can input a URL (website or social media profile) to scrape data. View history and delete past scrapings.
- **Login Screen**: Google and Facebook OAuth authentication options.

## Conclusion

This project demonstrates Flask, PostgreSQL integration, web scraping, and the use of Google and Facebook OAuth for user authentication. The application is containerized with Docker and includes basic CRUD operations for managing prompts and scraped data.