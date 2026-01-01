from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from .database import db
from .models import Comment, Incident, User

bp = Blueprint("bp", __name__)


@bp.before_request
@login_required
def requiere_login():
    pass


@bp.route("/")
def root():
    return redirect(url_for("bp.incidents"))


@bp.route("/about")
def about():
    return render_template("about.html")


@bp.route("/incidents/create", methods=["GET", "POST"])
def create_incident():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        severity = request.form["severity"]
        assignee = request.form["assignee"]
        if not title or not description or not severity:
            flash("All fields are required!", "error")
            return redirect(url_for("bp.create_incident"))
        new_incident = Incident(
            title=title,
            description=description,
            severity=severity,
            created_by_id=current_user.id,
            assigned_to_id=int(assignee) if assignee else None,
        )
        db.session.add(new_incident)
        db.session.commit()
        flash("Incident created successfully!", "success")
        return redirect(url_for("bp.incidents"))

    return render_template("create-incident.html", users=db.session.query(User).all())


@bp.route("/incidents")
def incidents():
    q = request.args.get("q", "").strip()
    if q:
        incident_id = q.lstrip("#")
        if incident_id.isdigit():
            incident = Incident.query.get(int(incident_id))
            if incident:
                return redirect(url_for("bp.incident_detail", incident_id=incident.id))
            flash("Incident not found.", "error")
            return redirect(url_for("bp.incidents"))
    incidents = Incident.query.order_by(Incident.created_at.desc()).all()
    return render_template("incidents.html", incidents=incidents)


@bp.route("/incidents/<int:incident_id>", methods=["GET", "POST"])
def incident_detail(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    comments = Comment.query.filter_by(incident_id=incident_id).order_by(Comment.created_at.desc()).all()
    return render_template("incident-detail.html", incident=incident, comments=comments, users=db.session.query(User).all())


@bp.route("/incidents/<int:incident_id>/update-status", methods=["POST"])
def update_status(incident_id):
    action = request.form.get("action")
    incident = Incident.query.get_or_404(incident_id)
    if action == "solve":
        incident.status = "Solved"
        comment_content = f"Incident solved by {current_user.name}."
        solver = User.query.get_or_404(current_user.id)
        incident.solved_by_id = solver.id
        flash("Incident marked as solved.", "success")
    elif action == "cancel":
        incident.status = "Cancelled"
        comment_content = f"Incident cancelled by {current_user.name}."
        flash("Incident marked as cancelled.", "success")
    else:
        flash("Invalid action.", "error")
        return redirect(url_for("bp.incident_detail", incident_id=incident_id))

    new_comment = Comment(content=comment_content, incident_id=incident_id, commented_by_id=current_user.id, is_system=True)
    db.session.add(new_comment)
    db.session.commit()

    return redirect(url_for("bp.incident_detail", incident_id=incident_id))


@bp.route("/incidents/<int:incident_id>/comment", methods=["POST"])
def comment_incident(incident_id):
    content = request.form["comment"]
    if not content:
        flash("Comment cannot be empty!", "error")
        return redirect(url_for("bp.incident_detail", incident_id=incident_id))
    new_comment = Comment(content=content, incident_id=incident_id, commented_by_id=current_user.id)
    db.session.add(new_comment)
    db.session.commit()
    flash("Comment added successfully!", "success")
    return redirect(url_for("bp.incident_detail", incident_id=incident_id))


@bp.route("/incidents/<int:incident_id>/reassign", methods=["POST"])
def reassign_incident(incident_id):
    reassigne_id = request.form["reassignee"]
    if not reassigne_id:
        incident = Incident.query.get_or_404(incident_id)
        incident.assigned_to_id = None
        comment_content = f"Incident Unassigned by {current_user.name}."
        new_comment = Comment(content=comment_content, incident_id=incident_id, commented_by_id=current_user.id, is_system=True)
        db.session.add(incident)
        db.session.add(new_comment)
        db.session.commit()
        flash("Incident unassigned", "error")
        return redirect(url_for("bp.incident_detail", incident_id=incident_id))
    incident = Incident.query.get_or_404(incident_id)
    incident.assigned_to_id = reassigne_id
    reassigne = User.query.get_or_404(reassigne_id)
    comment_content = f"Incident reassigned to {reassigne.name} by {current_user.name}."

    new_comment = Comment(content=comment_content, incident_id=incident_id, commented_by_id=current_user.id, is_system=True)
    db.session.add(incident)
    db.session.add(new_comment)
    db.session.commit()
    flash("Incident reassigned successfully", "success")
    return redirect(url_for("bp.incident_detail", incident_id=incident_id))


@bp.route("/health")
def health_check():
    return jsonify({"status": "ok", "message": "service is up"}), 200
