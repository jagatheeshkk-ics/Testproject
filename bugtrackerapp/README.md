# ELM Bug Tracking System

A small Flask app for logging, triaging, and sharing bugs with the development team.

## Features

- Individual login accounts per team member (register at `/register`, log in at `/login`)
- Update your own display name and password at `/account`
- **Users master** (`/users`) — view all accounts and manually add new ones (`/users/new`), independent of self-registration
- Log bugs with title, description, severity, status, reporter (your account), and assignee (any registered account)
- Bulk-import bugs from an Excel (`.xlsx`) file at `/bugs/import`
- Filter the bug list by status and severity
- Edit/update bug status as work progresses
- **Dashboard** (`/dashboard`) with KPI tiles, a daily-bug-count chart, and a bugs-by-severity chart
- **Send the bug list to the development team** via:
  - **Generate Report** (`/export/report`) — a clean, printable page (with the same charts as the dashboard) you can share the URL of, or print to PDF
  - **CSV export** (`/export/csv`) — a downloadable spreadsheet of the full bug list

## Local setup

```bash
pip install -r requirements.txt
python seed.py      # optional: adds sample accounts + bugs (password: changeme123)
python app.py
```

Then open http://127.0.0.1:5000 and log in (or register a new account).

## Hosting (e.g. Render)

The app is ready to deploy behind gunicorn and reads its config from environment
variables, so no code changes are needed to host it.

1. Push this repo to GitHub (already done if you're reading this from there).
2. On [render.com](https://render.com), **New → Web Service**, connect this repo.
3. Build command: `pip install -r requirements.txt`
   Start command: `gunicorn app:app --bind 0.0.0.0:$PORT` (also defined in `Procfile`,
   so Render should pick it up automatically).
4. Set environment variables:
   - `SECRET_KEY` — any random string (used to sign login sessions)
   - `DATABASE_URL` — optional; add a free Render Postgres instance and paste its
     connection string here for data that survives redeploys. If omitted, the app
     falls back to a local SQLite file, which **will not persist** across redeploys
     on most hosting platforms (their filesystems are ephemeral).
5. Deploy. On first boot the app creates its tables automatically
   (`db.create_all()`); run `python seed.py` once via a one-off shell/job on the
   host if you want the sample accounts and bugs.

## Project structure

```
app.py              Flask app, routes, and the User/Bug models
seed.py              Optional sample data loader
Procfile             Start command for gunicorn (used by Render/Heroku-style hosts)
templates/           Jinja2 templates (list, form, login/register, dashboard, report, import)
static/style.css     Styling
instance/bugs.db     SQLite database (created on first run, git-ignored)
```
