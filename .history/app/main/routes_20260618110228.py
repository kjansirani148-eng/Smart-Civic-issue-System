from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    if current_user.is_authenticated:
        if current_user.role == "admin":
            return redirect(url_for("admin.dashboard"))
        if current_user.role == "officer":
            return redirect(url_for("officer.dashboard"))
        return redirect(url_for("user.dashboard"))
    return render_template("index.html")


@main_bp.app_errorhandler(403)
def forbidden(error):
    return render_template("errors/403.html"), 403


@main_bp.app_errorhandler(404)
def not_found(error):
    return render_template("errors/404.html"), 404


@main_bp.app_errorhandler(500)
def internal_error(error):
    return render_template("errors/500.html"), 500
