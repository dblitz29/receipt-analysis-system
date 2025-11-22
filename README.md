#  Receipt Analysis System

This is a small web application for collecting and organizing food receipt data.  
Users can upload a receipt, the system reads the text, extracts the important fields, and stores everything in a local SQLite database.  
You can also ask simple questions and the app will convert the question into SQL automatically.

##  System Overview
![alt text](Assets\architectures.jpg "Title")


##  Features

- Upload and read receipt images  
- Extract vendor, date, items, and totals  
- Store structured data in SQLite  
- Ask natural-language questions and get SQL-generated answers  
- Containerized with Docker  
- Automated workflow that builds and tests the container  

##  Running Locally

```
pip install -r requirements.txt
python app.py
```

Open:  
**http://localhost:5000**

##  Running with Docker

Build:

```
docker build -t receipt-app .
```

Run:

```
docker run -p 5000:5000 --env-file .env receipt-app
```

On first startup, the container will create the database automatically if it doesn’t exist.

##  CI/CD Workflow

A GitHub Actions workflow is included.  
Every push to `main` will:

1. Build the Docker image  
2. Run the container  
3. Perform a small health check  

This confirms that the application still runs successfully.

##  Project Structure
```
app.py
database/
  ├─ db.py
  ├─ init_db.py
ocr/
  ├─ ocr_expense.py
  ├─ receipt_parser.py
query_engine/
  ├─ text_to_sql.py
  ├─ runner.py
templates/
static/
Dockerfile
entrypoint.sh
```

##  Notes
This project is kept intentionally small and focused, since it was built for a technical.  
The goal is to show a clean flow: upload → extract → parse → store → query.