# Employee Management API

![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![Flask](https://img.shields.io/badge/Flask-RESTX-blue.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)
![Render](https://img.shields.io/badge/Deployed_on-Render-success.svg)

A RESTful API built with **Flask-RESTX** for managing employees and departments. This project is designed with a modular architecture and deployed on Render.

🔗 **Live Demo**:  
👉 [empleados-backend-3b43.onrender.com](https://empleados-backend-3b43.onrender.com)

---

## 🚀 Features

- CRUD endpoints for **Employees** and **Departments**
- Modular architecture using **Namespaces**
- Lightweight **SQLite** database
- Custom CLI commands:
  - `flask init-db` to initialize database
  - `flask insert-data` to load sample data
- CORS enabled for frontend interaction
- `/health` endpoint for uptime monitoring
- Automated deployment using `render.yaml`

---

## 📁 Project Structure

.
├── app/
│ ├── init.py
│ ├── db/
│ │ └── init_db.py
│ ├── routes/
│ │ ├── empleados.py
│ │ ├── departamentos.py
│ │ └── health.py
│ └── models/
│ └── schemas.py
├── empleados.db
├── wsgi.py
├── render.yaml
├── requirements.txt
└── README.md

---

## 🧑‍💻 Local Setup

```bash
# Clone the repository
git clone https://github.com/Ludvin7x/empleados-Backend.git
cd your-repo

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize the database and insert initial data
flask init-db
flask insert-data

# Start the development server
flask run
```

## 📡 Available Endpoints
GET /api/empleados/

POST /api/empleados/

PUT /api/empleados/<id>

DELETE /api/empleados/<id>

GET /api/departamentos/

POST /api/departamentos/

GET /health — Health check

Swagger UI documentation is available at the root URL.

## ⚙️ Deployment
The project is deployed on Render using render.yaml to automate:

Dependency installation

Database setup

Sample data insertion

Environment variable configuration

No additional manual steps are required after pushing to GitHub.

## 🛠️ Tech Stack
Python 3.10+

Flask + Flask-RESTX

SQLite

Flask-CORS

Gunicorn

Render