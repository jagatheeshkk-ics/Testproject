# Bug Tracker

A small Flask app for logging, triaging, and sharing bugs with the development team.

## Features

- Log bugs with title, description, severity, status, reporter, and assignee
- Filter the bug list by status and severity
- Edit/update bug status as work progresses
- **Send the bug list to the development team** via:
  - **Report view** (`/export/report`) — a clean, printable page you can share the URL of, or print to PDF
  - **CSV export** (`/export/csv`) — a downloadable spreadsheet of the full bug list

## Setup

```bash
pip install -r requirements.txt
python seed.py      # optional: adds a few sample bugs
python app.py
```

Then open http://127.0.0.1:5000

## Project structure

```
app.py              Flask app, routes, and the Bug model
seed.py              Optional sample data loader
templates/           Jinja2 templates (list, form, printable report)
static/style.css     Styling
bugs.db              SQLite database (created on first run)
```
