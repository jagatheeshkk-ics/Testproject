import csv
import io
from datetime import datetime

from flask import Flask, redirect, render_template, request, Response, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bugs.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

SEVERITIES = ["Low", "Medium", "High", "Critical"]
STATUSES = ["Open", "In Progress", "Resolved", "Closed"]


class Bug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False, default="")
    severity = db.Column(db.String(20), nullable=False, default="Medium")
    status = db.Column(db.String(20), nullable=False, default="Open")
    reporter = db.Column(db.String(100), nullable=False, default="")
    assignee = db.Column(db.String(100), nullable=False, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    status_filter = request.args.get("status", "")
    severity_filter = request.args.get("severity", "")

    query = Bug.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    if severity_filter:
        query = query.filter_by(severity=severity_filter)

    bugs = query.order_by(Bug.created_at.desc()).all()

    counts = {status: Bug.query.filter_by(status=status).count() for status in STATUSES}

    return render_template(
        "index.html",
        bugs=bugs,
        statuses=STATUSES,
        severities=SEVERITIES,
        status_filter=status_filter,
        severity_filter=severity_filter,
        counts=counts,
    )


@app.route("/bugs/new", methods=["GET", "POST"])
def new_bug():
    if request.method == "POST":
        bug = Bug(
            title=request.form["title"].strip(),
            description=request.form.get("description", "").strip(),
            severity=request.form.get("severity", "Medium"),
            status=request.form.get("status", "Open"),
            reporter=request.form.get("reporter", "").strip(),
            assignee=request.form.get("assignee", "").strip(),
        )
        db.session.add(bug)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("bug_form.html", bug=None, severities=SEVERITIES, statuses=STATUSES)


@app.route("/bugs/<int:bug_id>/edit", methods=["GET", "POST"])
def edit_bug(bug_id):
    bug = Bug.query.get_or_404(bug_id)

    if request.method == "POST":
        bug.title = request.form["title"].strip()
        bug.description = request.form.get("description", "").strip()
        bug.severity = request.form.get("severity", bug.severity)
        bug.status = request.form.get("status", bug.status)
        bug.reporter = request.form.get("reporter", "").strip()
        bug.assignee = request.form.get("assignee", "").strip()
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("bug_form.html", bug=bug, severities=SEVERITIES, statuses=STATUSES)


@app.route("/bugs/<int:bug_id>/delete", methods=["POST"])
def delete_bug(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    db.session.delete(bug)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/export/csv")
def export_csv():
    bugs = Bug.query.order_by(Bug.created_at.desc()).all()

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(
        ["ID", "Title", "Description", "Severity", "Status", "Reporter", "Assignee", "Created At", "Updated At"]
    )
    for bug in bugs:
        writer.writerow(
            [
                bug.id,
                bug.title,
                bug.description,
                bug.severity,
                bug.status,
                bug.reporter,
                bug.assignee,
                bug.created_at.strftime("%Y-%m-%d %H:%M"),
                bug.updated_at.strftime("%Y-%m-%d %H:%M"),
            ]
        )

    filename = f"bug_list_{datetime.utcnow().strftime('%Y%m%d_%H%M')}.csv"
    return Response(
        buffer.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@app.route("/export/report")
def export_report():
    bugs = Bug.query.order_by(Bug.severity.desc(), Bug.created_at.desc()).all()
    return render_template("report.html", bugs=bugs, generated_at=datetime.utcnow())


if __name__ == "__main__":
    app.run(debug=True)
