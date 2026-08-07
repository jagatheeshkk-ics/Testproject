# ELM Bug Tracking System

A small Flask app for logging, triaging, and sharing bugs with the development team.

## Features

- Individual login accounts per team member (register at `/register`, log in at `/login`)
- Update your own display name and password at `/account`
- **Users master** (`/users`) — view all accounts and manually add new ones (`/users/new`), independent of self-registration
- **Status master** (`/statuses`) — statuses are a managed table (seeded with Open/In Progress/Resolved/Closed) rather than hardcoded, so custom statuses can be added
- **Project master** (`/projects`) — bugs can optionally be filed against a project
- Log bugs with title, description, severity, status, project, reporter (your account), assignee (any registered account), and an optional file attachment (10 MB max)
- Bulk-import bugs from an Excel (`.xlsx`) file at `/bugs/import`
- Filter the bug list by status, severity, and project
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
   - `PYTHON_VERSION` — `3.11.9` (also pinned in `.python-version`). **Required if
     using Postgres**: `psycopg2-binary` does not yet ship working wheels for the
     very latest Python releases (e.g. 3.14), which fails at import time with
     `undefined symbol: _PyInterpreterState_Get`. Pinning to 3.11 avoids this.
   - `DATABASE_URL` — optional; add a free Render Postgres instance and paste its
     connection string here for data that survives redeploys. If omitted, the app
     falls back to a local SQLite file, which **will not persist** across redeploys
     on most hosting platforms (their filesystems are ephemeral).
5. Deploy. On first boot the app creates its tables automatically
   (`db.create_all()`); run `python seed.py` once via a one-off shell/job on the
   host if you want the sample accounts and bugs.

**Bug attachments have the same ephemeral-storage caveat as SQLite.** Uploaded
files are saved to `instance/uploads/` on local disk — fine for a normal server,
but on platforms with ephemeral filesystems (Render's free tier included) they
will be lost on redeploy/restart, same as SQLite data would be. If that matters,
the fix is the same as for the database: move to a persistent volume or object
storage (e.g. S3) — not implemented here since it's an added dependency this
app doesn't otherwise need.

## Project structure

```
app.py              Flask app, routes, and the User/Bug/Status/Project models
seed.py              Optional sample data loader
Procfile             Start command for gunicorn (used by Render/Heroku-style hosts)
.python-version      Pins the Python version for hosts that read it (e.g. Render)
templates/           Jinja2 templates (list, form, login/register, dashboard, report, import, masters)
static/style.css     Styling
instance/bugs.db     SQLite database (created on first run, git-ignored)
```
