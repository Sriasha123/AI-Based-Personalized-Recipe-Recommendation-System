"""
SIMPLE FILE CREATOR
Save this as: create_files.py
Run in: Desktop/Final/recipe-recommendation-system/
"""

import os

# Change to the directory where you want to create files
# Make sure you're in the recipe-recommendation-system folder
print("Creating files in:", os.getcwd())
print("\nMake sure you're in the 'recipe-recommendation-system' folder!")
print("If not, navigate there first: cd Desktop/Final/recipe-recommendation-system\n")

input("Press Enter to continue...")

files = {
    # Backend files
    "backend/requirements.txt": """fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pydantic==2.5.0
pydantic-settings==2.1.0
pandas==2.1.3
numpy==1.26.2
scikit-learn==1.3.2
python-dotenv==1.0.0""",

    "backend/.env": """DATABASE_URL=postgresql://postgres:password@localhost:5432/recipe_db
SECRET_KEY=super-secret-key-change-this-in-production-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=43200""",

    "backend/app/__init__.py": "",
    "backend/app/auth/__init__.py": "",
    "backend/app/recipes/__init__.py": "",
    "backend/app/reviews/__init__.py": "",
    "backend/app/recommendations/__init__.py": "",
    "backend/app/meal_planner/__init__.py": "",
    "backend/app/grocery/__init__.py": "",

    "backend/app/config.py": """from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200
    class Config:
        env_file = ".env"

settings = Settings()""",

    "backend/app/database.py": """from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()""",

    "backend/data/raw/README.txt": """PUT YOUR DATASETS HERE:
- recipes.csv
- reviews.csv""",

    "README.md": """# AI Recipe Recommendation System

## Quick Start

1. Place datasets in: backend/data/raw/
2. Setup backend: cd backend && pip install -r requirements.txt
3. Setup database: createdb recipe_db
4. Run backend: uvicorn app.main:app --reload
5. Setup frontend: cd frontend && npm install && npm run dev
6. Open: http://localhost:3000

## See full documentation in SETUP_INSTRUCTIONS.md
""",

    "frontend/package.json": """{
  "name": "recipe-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.2",
    "lucide-react": "^0.294.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.3.6",
    "vite": "^5.0.8"
  }
}""",

    "frontend/index.html": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>AI Recipe Recommendations</title>
</head>
<body>
  <div id="root"></div>
  <script type="module" src="/src/main.jsx"></script>
</body>
</html>""",
}

print("Creating files...\n")

for filepath, content in files.items():
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Created: {filepath}")
    except Exception as e:
        print(f"❌ Error creating {filepath}: {e}")

print("\n✅ Basic files created!")
print("\nNEXT: I'll provide the remaining files separately.")
print("Check if these files were created successfully.")