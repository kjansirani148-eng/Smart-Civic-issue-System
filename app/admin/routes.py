from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.models import Category, Complaint, ComplaintStatus, Notification, Officer, User

def admin_required():
    if not current_user.is_authenticated or current_user.role != "admin":
        abort(403)


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/dashboard")
@login_required
def dashboard():
    admin_required()
    total = Complaint.query.count()
    open_count = Complaint.query.filter(Complaint.status.has(name="Open")).count()
    in_progress = Complaint.query.filter(Complaint.status.has(name="In Progress")).count()
    resolved = Complaint.query.filter(Complaint.status.has(name="Resolved")).count()
    category_stats = (
        db.session.query(Category.name, db.func.count(Complaint.id))
        .join(Complaint, Complaint.category_id == Category.id)
        .group_by(Category.name)
        .all()
    )
    trend_data = (
        db.session.query(Complaint.created_at, db.func.count(Complaint.id))
        .group_by(db.func.date(Complaint.created_at))
        .order_by(db.func.date(Complaint.created_at))
        .all()
    )
    return render_template(
        "admin/dashboard.html",
        total=total,
        open_count=open_count,
        in_progress=in_progress,
        resolved=resolved,
        category_stats=category_stats,
        trend_data=trend_data,
    )


@admin_bp.route("/users")
@login_required
def manage_users():
    admin_required()
    users = User.query.filter(User.role == "citizen").order_by(User.created_at.desc()).all()
    return render_template("admin/manage_users.html", users=users)


@admin_bp.route("/officers", methods=["GET", "POST"])
@login_required
def manage_officers():
    admin_required()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        department = request.form.get("department", "").strip()
        assigned_area = request.form.get("assigned_area", "").strip()

        if not name or not email or not password:
            flash("Officer name, email and password are required.", "danger")
            return redirect(url_for("admin.manage_officers"))

        if User.query.filter_by(email=email).first():
            flash("Email is already registered.", "danger")
            return redirect(url_for("admin.manage_officers"))

        user = User(name=name, email=email, role="officer")
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        officer = Officer(user_id=user.id, department=department, assigned_area=assigned_area)
        db.session.add(officer)
        db.session.commit()

        flash("Officer account created successfully.", "success")
        return redirect(url_for("admin.manage_officers"))

    officers = Officer.query.order_by(Officer.created_at.desc()).all()
    return render_template("admin/manage_officers.html", officers=officers)


@admin_bp.route("/complaints")
@login_required
def manage_complaints():
    admin_required()
    complaints = Complaint.query.order_by(Complaint.created_at.desc()).all()
    statuses = ComplaintStatus.query.order_by(ComplaintStatus.id).all()
    return render_template("admin/manage_complaints.html", complaints=complaints, statuses=statuses)


@admin_bp.route("/complaints/update/<int:complaint_id>", methods=["POST"])
@login_required
def update_complaint_status(complaint_id):
    admin_required()
    complaint = Complaint.query.get_or_404(complaint_id)
    status_id = request.form.get("status_id")
    officer_id = request.form.get("officer_id")

    if status_id:
        complaint.status_id = int(status_id)
    if officer_id:
        complaint.officer_id = int(officer_id)

    db.session.commit()
    flash("Complaint updated.", "success")
    return redirect(url_for("admin.manage_complaints"))


@admin_bp.route("/categories", methods=["GET", "POST"])
@login_required
def manage_categories():
    admin_required()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()

        if not name:
            flash("Category name is required.", "danger")
            return redirect(url_for("admin.manage_categories"))

        if Category.query.filter_by(name=name).first():
            flash("Category already exists.", "danger")
            return redirect(url_for("admin.manage_categories"))

        category = Category(name=name, description=description)
        db.session.add(category)
        db.session.commit()
        flash("Category created.", "success")
        return redirect(url_for("admin.manage_categories"))

    categories = Category.query.order_by(Category.name).all()
    return render_template("admin/categories.html", categories=categories)


@admin_bp.route("/analytics")
@login_required
def analytics():
    admin_required()
    category_stats = (
        db.session.query(Category.name, db.func.count(Complaint.id))
        .join(Complaint, Complaint.category_id == Category.id)
        .group_by(Category.name)
        .all()
    )
    status_stats = (
        db.session.query(ComplaintStatus.name, db.func.count(Complaint.id))
        .join(Complaint, Complaint.status_id == ComplaintStatus.id)
        .group_by(ComplaintStatus.name)
        .all()
    )
    return render_template(
        "admin/analytics.html",
        category_stats=category_stats,
        status_stats=status_stats,
    )
