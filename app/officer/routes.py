from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.models import Complaint, ComplaintStatus, Notification, Officer
from app.utils import allowed_file, upload_file_to_s3

officer_bp = Blueprint("officer", __name__, url_prefix="/officer")


def officer_required():
    if not current_user.is_authenticated or current_user.role != "officer":
        abort(403)


@officer_bp.route("/dashboard")
@login_required
def dashboard():
    officer_required()
    officer_profile = Officer.query.filter_by(user_id=current_user.id).first()
    assigned = Complaint.query.filter_by(officer_id=officer_profile.id).all() if officer_profile else []
    status_counts = {
        c.name: Complaint.query.filter_by(officer_id=officer_profile.id, status_id=c.id).count()
        for c in ComplaintStatus.query.all()
    }
    return render_template(
        "officer/dashboard.html",
        assigned=assigned,
        status_counts=status_counts,
    )


@officer_bp.route("/assigned")
@login_required
def assigned_list():
    officer_required()
    officer_profile = Officer.query.filter_by(user_id=current_user.id).first()
    if not officer_profile:
        abort(403)
    complaints = Complaint.query.filter_by(officer_id=officer_profile.id).order_by(Complaint.updated_at.desc()).all()
    return render_template("officer/assigned.html", complaints=complaints)


@officer_bp.route("/assign/<int:complaint_id>")
@login_required
def assign_self(complaint_id):
    officer_required()
    officer_profile = Officer.query.filter_by(user_id=current_user.id).first()
    complaint = Complaint.query.get_or_404(complaint_id)
    if complaint.officer_id:
        flash("Complaint is already assigned.", "warning")
        return redirect(url_for("officer.dashboard"))
    complaint.officer_id = officer_profile.id
    complaint.status_id = ComplaintStatus.query.filter_by(name="In Progress").first().id
    db.session.commit()
    flash("Complaint assigned to you.", "success")
    return redirect(url_for("officer.assigned_list"))


@officer_bp.route("/complaint/<int:complaint_id>", methods=["GET", "POST"])
@login_required
def complaint_detail(complaint_id):
    officer_required()
    officer_profile = Officer.query.filter_by(user_id=current_user.id).first()
    complaint = Complaint.query.get_or_404(complaint_id)
    if complaint.officer_id != officer_profile.id:
        abort(403)

    if request.method == "POST":
        status_id = request.form.get("status_id")
        remark = request.form.get("remark", "").strip()
        resolution_image = request.files.get("resolution_image")

        if status_id:
            complaint.status_id = int(status_id)
        complaint.remark = remark

        if resolution_image and resolution_image.filename:
            if not allowed_file(resolution_image.filename):
                flash("Resolution image must be JPG, PNG, or GIF.", "danger")
                return render_template("officer/complaint_detail.html", complaint=complaint)
            try:
                complaint.resolution_image_url = upload_file_to_s3(resolution_image)
            except Exception:
                flash("Unable to upload resolution image.", "warning")

        db.session.commit()
        notification = Notification(
            user_id=complaint.user_id,
            complaint_id=complaint.id,
            message=f"Officer updated complaint status to {complaint.status.name}.",
        )
        db.session.add(notification)
        db.session.commit()
        flash("Complaint updated successfully.", "success")
        return redirect(url_for("officer.complaint_detail", complaint_id=complaint.id))

    statuses = ComplaintStatus.query.order_by(ComplaintStatus.id).all()
    return render_template("officer/complaint_detail.html", complaint=complaint, statuses=statuses)
