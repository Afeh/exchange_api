# Country Currency & Exchange API

This is a RESTful API that fetches country data from `restcountries.com` and exchange rates from `open.er-api.com`, computes an estimated GDP, and caches the results in a MySQL database. It also generates a summary image of the cached data.

## Features

- **Data Caching**: Fetches and stores data locally to reduce reliance on external APIs.
- **CRUD Operations**: Provides endpoints to list, retrieve, and delete country data.
- **Dynamic Filtering & Sorting**: Supports filtering by region/currency and sorting by GDP.
- **Status Monitoring**: An endpoint to check the cache status and total countries.
- **Image Generation**: Automatically creates and serves a PNG image summarizing the data.

## API Endpoints

- `POST /countries/refresh`: Fetches the latest data from external APIs, updates the database, and regenerates the summary image.
- `GET /countries`: Retrieves all cached countries.
  - Query Parameters:
    - `?region={region_name}` (e.g., `Africa`)
    - `?currency={currency_code}` (e.g., `NGN`)
    - `?sort=gdp_desc`
- `GET /countries/{name}`: Retrieves a single country by its name (case-insensitive).
- `DELETE /countries/{name}`: Deletes a country from the cache.
- `GET /status`: Returns the total number of countries in the cache and the timestamp of the last successful refresh.
- `GET /countries/image`: Serves the generated summary image.

## Setup Instructions

### Prerequisites

- Python 3.8+
- MySQL Server
- A font file for image generation (e.g., DejaVuSans). The path is configured in `app/image_generator.py`.

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <repo-name>
```

### 2. Install Dependencies

It is recommended to use a virtual environment.

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root of the project by copying the example:

```bash
cp .env.example .env
```

Edit the `.env` file and set your `DATABASE_URL`.

**Example for MySQL:**
`DATABASE_URL="mysql+pymysql://user:password@host:port/database_name"`

### 4. Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.
Interactive documentation (Swagger UI) is available at `http://127.0.0.1:8000/docs`.