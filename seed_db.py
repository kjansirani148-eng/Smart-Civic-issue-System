from app import create_app, db
from app.models import User, Officer, Category, ComplaintStatus, Complaint
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    print("Initializing database tables...")
    
    ()
    print("Tables created successfully!")

    # Seed statuses if not present
    statuses = [
        ('Open', 'Complaint has been filed and is waiting for assignment.'),
        ('In Progress', 'Complaint has been assigned and work is underway.'),
        ('Resolved', 'Complaint has been addressed and resolved.')
    ]
    for status_name, desc in statuses:
        if not ComplaintStatus.query.filter_by(name=status_name).first():
            db.session.add(ComplaintStatus(name=status_name, description=desc))
            print(f"Added status: {status_name}")

    # Seed categories if not present
    categories = [
        ('Road damage', 'Broken roads, potholes, and pavement failures.'),
        ('Garbage issues', 'Trash collection, overflowing bins, and littering.'),
        ('Street light failure', 'Non-functioning or flickering street lights.'),
        ('Water leakage', 'Broken pipes, leaks, or flooding issues.'),
        ('Drainage blockage', 'Clogged drains and stormwater backups.')
    ]
    for cat_name, desc in categories:
        if not Category.query.filter_by(name=cat_name).first():
            db.session.add(Category(name=cat_name, description=desc))
            print(f"Added category: {cat_name}")

    db.session.commit()

    # Seed users if not present
    # Default password is 'password'
    pw_hash = generate_password_hash('password')

    users_data = [
        ('Admin User', 'admin@smartcivic.local', 'admin', '0000000000', 'City Hall'),
        ('Jane Citizen', 'jane.user@example.com', 'citizen', '555-0123', '12 Civic Lane'),
        ('Officer Joe', 'joe.officer@example.com', 'officer', '555-0456', 'Central Station')
    ]

    for name, email, role, phone, address in users_data:
        if not User.query.filter_by(email=email).first():
            user = User(
                name=name,
                email=email,
                password_hash=pw_hash,
                role=role,
                phone=phone,
                address=address
            )
            db.session.add(user)
            print(f"Added user: {email} ({role})")

    db.session.commit()

    # Seed officer profile
    officer_user = User.query.filter_by(email='joe.officer@example.com').first()
    if officer_user and not Officer.query.filter_by(user_id=officer_user.id).first():
        officer = Officer(
            user_id=officer_user.id,
            department='Public Works',
            assigned_area='Downtown'
        )
        db.session.add(officer)
        print("Added officer profile for Joe")

    db.session.commit()

    # Seed complaints if none exist
    if Complaint.query.count() == 0:
        jane = User.query.filter_by(email='jane.user@example.com').first()
        road_damage = Category.query.filter_by(name='Road damage').first()
        street_light = Category.query.filter_by(name='Street light failure').first()
        status_open = ComplaintStatus.query.filter_by(name='Open').first()
        status_progress = ComplaintStatus.query.filter_by(name='In Progress').first()
        officer = Officer.query.join(User).filter(User.email == 'joe.officer@example.com').first()

        if jane and road_damage and status_open:
            c1 = Complaint(
                user_id=jane.id,
                category_id=road_damage.id,
                status_id=status_open.id,
                description='Pothole near the main street intersection.',
                latitude=37.7749,
                longitude=-122.4194,
                image_url='https://via.placeholder.com/640x360.png'
            )
            db.session.add(c1)
            print("Added first sample complaint")

        if jane and street_light and status_progress and officer:
            c2 = Complaint(
                user_id=jane.id,
                category_id=street_light.id,
                status_id=status_progress.id,
                officer_id=officer.id,
                description='Streetlight remains dark for three nights.',
                latitude=37.7750,
                longitude=-122.4180,
                image_url='https://via.placeholder.com/640x360.png'
            )
            db.session.add(c2)
            print("Added second sample complaint")

        db.session.commit()

    print("Database seeding completed successfully!")
