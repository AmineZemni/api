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


Testing the API Using Swagger.

FastAPI provides an interactive API documentation via Swagger UI, making it easy to test endpoints without external tools.

Steps:
1- Start the FastAPI server in your teminal with the command: 

        uvicorn app.main:app --reload

2- Open your browser and go to: http://127.0.0.1:8000/docs

3- Find the API and TY

4- Click on Try it out → Enter values for value1 and value2 → Click Execute.


# Run Tests

pytest
