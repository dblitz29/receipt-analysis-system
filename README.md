Receipt Analysis System

This project is a small web app that lets users upload food receipts and turn them into structured data. The app extracts the vendor, date, items, and totals, stores everything in a local database, and also supports simple natural-language questions like “What did I buy yesterday?” using a text-to-SQL module.

Features
Upload receipt through a simple UI
OCR step that reads the text from the receipt
Parse the extracted fields into a clean format
Store data in a SQLite database
Convert user questions into SQL and return the results
Runs inside a Docker container
CI workflow that builds and smoke-tests the container