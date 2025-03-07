# AI-Powered Interview Question Generator Frontend

This is a Streamlit-based frontend for the **AI-Powered Interview Question Generator** app. Currently, the application is run locally.

---

## Getting Started

### 1. Create a Python Virtual Environment

First, create a python virtual environment in the root workspace directory:

```bash
python -m venv .venv/interview-generator-frontend
source .venv/interview-generator-frontend/bin/activate  # On Windows: .venv\interview-generator-frontend\Scripts\activate
pip install -r  ./frontend/requirements.txt
```

### 2. Run the Application

Run the application by using the following command: (Ensure that the FAST API is running)

```bash
streamlit run ./frontend/Home.py
```

##### For Admin
```bash
streamlit run .\frontend\admin\Admin.py
```

The API will be available at [**Streamlit app**](http://localhost:8501)

---

**Happy Coding! 🚀**
