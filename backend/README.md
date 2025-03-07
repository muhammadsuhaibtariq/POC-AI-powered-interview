# AI-Powered Interview Question Generator API

This is a Python FastAPI backend for **AI-Powered Interview Question Generator** App. Till now the APIs are called from the Swagger.

---

## Getting Started

### 1. Create a Python Virtual Environment

First, create a python virtual environment in the root workspace directory:

```bash
python -m venv .venv/interview-generator-backend
source .venv/interview-generator-backend/bin/activate  # On Windows: .venv\interview-generator-backend\Scripts\activate
pip install -r  ./backend/requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the root of the backend project directory with the following required variables:

```plaintext
OPENAI_API_KEY="{Your OpenAI API Key}"
MONGODB_URI_FASTAPI="mongodb+srv://{Your MongoDB Username}:{Your MongoDB Password}@{Your MongoDB Cluster}.mongodb.net"
```

### 3. Run the Application

Run the application by pressing `F5` in VS Code. Ensure that the `.env` file is also in the root of the project directory and that the virtual environment (`venv`) is set to `sa-system-backend`.

or using:

```bash
uvicorn backend.app.main:app --reload
```

The API will be available at [**Swagger UI**](http://localhost:8000/docs)

## API Documentation

For complete API documentation, visit `/docs` when the server is running. This provides an interactive documentation of all available endpoints and their parameters.


## Linting

### 1. Install Linting Tools

```bash
pip install flake8==7.1.1
```

### 2. Run Linting

From the backend directory:

```bash
flake8 --disable-noqa --ignore E128,E302,E305,W292,BLK100,W503 --max-line-length 120 .
```

Or from the project root directory:

```bash
flake8 --disable-noqa --ignore E128,E302,E305,W292,BLK100,W503 --max-line-length 120 --exclude=.venv backend
```
## Deployment

#### For local development, use the `.env` file as described in the setup section.

---

**Happy Coding! 🚀**
