# IFRS17-API (FastAPI Backend)

This is a FastAPI-based backend for IFRS17-API, using PostgreSQL, SQLAlchemy ORM, and Docker for containerization.

## 📂 Project Structure

tree

# Install Dependencies using conda for local development

conda create --name fastapi_env python=3.11

conda activate fastapi_env

pip install -r requirements.txt

# Run The Application 

uvicorn app.main:app --reload

API available at http://127.0.0.1:8000

# Run Tests

pytest
