"""Populate the tracker with sample bugs so the list has something to send."""
from app import Bug, app, db

SAMPLE_BUGS = [
    dict(
        title="Login page crashes on empty password submit",
        description="Submitting the login form with an empty password field throws a 500 error instead of a validation message.",
        severity="Critical",
        status="Open",
        reporter="AGGARS29@gmail.com",
        assignee="Dev Team",
    ),
    dict(
        title="Dashboard chart mislabels Q3 revenue",
        description="The revenue chart on the dashboard shows Q3 data under the Q2 label.",
        severity="High",
        status="In Progress",
        reporter="AGGARS29@gmail.com",
        assignee="Dev Team",
    ),
    dict(
        title="Profile avatar upload accepts non-image files",
        description="Uploading a .txt file as an avatar is accepted silently and breaks the profile page layout.",
        severity="Medium",
        status="Open",
        reporter="AGGARS29@gmail.com",
        assignee="Dev Team",
    ),
    dict(
        title="Footer copyright year is hardcoded",
        description="Footer still shows a fixed past year instead of the current year.",
        severity="Low",
        status="Open",
        reporter="AGGARS29@gmail.com",
        assignee="Dev Team",
    ),
]

with app.app_context():
    db.create_all()
    if Bug.query.count() == 0:
        for data in SAMPLE_BUGS:
            db.session.add(Bug(**data))
        db.session.commit()
        print(f"Seeded {len(SAMPLE_BUGS)} sample bugs.")
    else:
        print("Bugs already exist, skipping seed.")
