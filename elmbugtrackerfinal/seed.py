"""Populate the tracker with sample accounts and bugs so there's something to send."""
from app import Bug, User, app, db

SAMPLE_USERS = [
    dict(username="aggars29", display_name="A. Aggarwal", password="changeme123"),
    dict(username="dev.alice", display_name="Alice Chen", password="changeme123"),
    dict(username="dev.bob", display_name="Bob Martinez", password="changeme123"),
]

with app.app_context():
    db.create_all()

    users = {}
    if User.query.count() == 0:
        for data in SAMPLE_USERS:
            user = User(username=data["username"], display_name=data["display_name"])
            user.set_password(data["password"])
            db.session.add(user)
            users[data["username"]] = user
        db.session.commit()
        print(f"Seeded {len(SAMPLE_USERS)} accounts (password for all: changeme123).")
    else:
        print("Accounts already exist, skipping user seed.")
        users = {u.username: u for u in User.query.all()}

    reporter = users.get("aggars29") or User.query.first()
    alice = users.get("dev.alice")
    bob = users.get("dev.bob")

    SAMPLE_BUGS = [
        dict(
            title="Login page crashes on empty password submit",
            description="Submitting the login form with an empty password field throws a 500 error instead of a validation message.",
            severity="Critical",
            status="Open",
            assignee=alice,
        ),
        dict(
            title="Dashboard chart mislabels Q3 revenue",
            description="The revenue chart on the dashboard shows Q3 data under the Q2 label.",
            severity="High",
            status="In Progress",
            assignee=bob,
        ),
        dict(
            title="Profile avatar upload accepts non-image files",
            description="Uploading a .txt file as an avatar is accepted silently and breaks the profile page layout.",
            severity="Medium",
            status="Open",
            assignee=alice,
        ),
        dict(
            title="Footer copyright year is hardcoded",
            description="Footer still shows a fixed past year instead of the current year.",
            severity="Low",
            status="Open",
            assignee=bob,
        ),
    ]

    if Bug.query.count() == 0:
        for data in SAMPLE_BUGS:
            assignee = data.pop("assignee")
            db.session.add(Bug(reporter_id=reporter.id, assignee_id=assignee.id if assignee else None, **data))
        db.session.commit()
        print(f"Seeded {len(SAMPLE_BUGS)} sample bugs.")
    else:
        print("Bugs already exist, skipping bug seed.")
