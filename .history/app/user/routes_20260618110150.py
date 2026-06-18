from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.models import Category, Complaint, ComplaintStatus, Notification
from app.utils import allowed_file, upload_file_to_s3

user_bp = Blueprint("user", __name__, url_prefix="/user")


def citizen_required():
    if not current_user.is_authenticated or current_user.role != "citizen":
        abort(403)


@user_bp.route("/dashboard")
@login_required
def dashboard():
    citizen_required()
    complaints = Complaint.query.filter_by(user_id=current_user.id).order_by(Complaint.created_at.desc()).all()
    status_counts = {
        c.name: Complaint.query.filter_by(user_id=current_user.id, status_id=c.id).count()
        for c in ComplaintStatus.query.all()
    }
    return render_template(
        "user/dashboard.html",
        complaints=complaints,
        status_counts=status_counts,
    )


@user_bp.route("/report", methods=["GET", "POST"])
@login_required
def report():
    citizen_required()
    categories = Category.query.order_by(Category.name).all()

    if request.method == "POST":
        category_id = request.form.get("category_id")
        description = request.form.get("description", "").strip()
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")
        image = request.files.get("image")

        if not category_id or not description:
            flash("Please complete the form before submitting.", "danger")
            return render_template("user/report.html", categories=categories)

        category = Category.query.get(category_id)
        if not category:
            flash("Category not found.", "danger")
            return render_template("user/report.html", categories=categories)

        image_url = None
        if image and image.filename:
            if not allowed_file(image.filename):
                flash("Only JPG, PNG and GIF images are permitted.", "danger")
                return render_template("user/report.html", categories=categories)
            try:
                image_url = upload_file_to_s3(image)
            except Exception:
                flash("Unable to upload image. Please try again.", "warning")

        default_status = ComplaintStatus.query.filter_by(name="Open").first()
        complaint = Complaint(
            user_id=current_user.id,
            category_id=category.id,
            status_id=default_status.id if default_status else 1,
            description=description,
            latitude=float(latitude) if latitude else None,
            longitude=float(longitude) if longitude else None,
            image_url=image_url,
        )
        db.session.add(complaint)
        db.session.commit()

        notification = Notification(
            user_id=current_user.id,
            complaint_id=complaint.id,
            message="Your complaint has been submitted and is awaiting assignment.",
        )
        db.session.add(notification)
        db.session.commit()

        flash("Complaint submitted successfully.", "success")
        return redirect(url_for("user.dashboard"))

    return render_template("user/report.html", categories=categories)


@user_bp.route("/complaints")
@login_required
def my_complaints():
    citizen_required()
    complaints = Complaint.query.filter_by(user_id=current_user.id).order_by(Complaint.updated_at.desc()).all()
    return render_template("user/complaints.html", complaints=complaints)


@user_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    citizen_required()
    if request.method == "POST":
        current_user.name = request.form.get("name", current_user.name).strip()
        current_user.phone = request.form.get("phone", current_user.phone)
        current_user.address = request.form.get("address", current_user.address)
        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for("user.profile"))

    return render_template("user/profile.html")


@user_bp.route("/nearby")
@login_required
def nearby():
    citizen_required()
    lat = request.args.get("lat", type=float)
    lng = request.args.get("lng", type=float)
    nearby_complaints = []

    if lat is not None and lng is not None:
        complaints = Complaint.query.filter(Complaint.latitude.isnot(None), Complaint.longitude.isnot(None)).all()
        for complaint in complaints:
            distance = ((complaint.latitude - lat) ** 2 + (complaint.longitude - lng) ** 2) ** 0.5
            if distance <= 0.05:
                nearby_complaints.append(complaint)

    return render_template("user/nearby.html", complaints=nearby_complaints)
