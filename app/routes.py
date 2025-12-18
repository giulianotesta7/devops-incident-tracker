from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from models import Incident, Comment
from database import db
from flask_login import current_user, login_required

bp = Blueprint('bp', __name__)

@bp.before_request
@login_required
def login_required():
    pass

@bp.route('/')
def root():
    return redirect(url_for('bp.incidents'))

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/incidents/create', methods=['GET', 'POST'])
def create_incident():
    if request.method == 'POST':
        tittle=request.form['title']
        description=request.form['description']
        severity=request.form['severity']
        if not tittle or not description or not severity:
            flash("All fields are required!", "error")
            return redirect(url_for('bp.create_incident'))
        else:
            new_incident = Incident(title=tittle, description=description, severity=severity, created_by_id=current_user.id)  
            db.session.add(new_incident)
            db.session.commit()
            flash("Incident created successfully!", "success")
            return redirect(url_for('bp.create_incident'))
    


    return render_template('create-incident.html')

@bp.route('/incidents')
def incidents():
    incidents = Incident.query.order_by(Incident.created_at.desc()).all()
    return render_template('incidents.html', incidents=incidents)


@bp.route('/incidents/<int:incident_id>', methods=['GET', 'POST'])
def incident_detail(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    comments = (Comment.query
                .filter_by(incident_id=incident_id)
                .order_by(Comment.created_at.desc())
                .all())
    return render_template('incident-detail.html', incident=incident, comments=comments)

@bp.route('/incidents/<int:incident_id>/update-status', methods=['POST'])
def solve_incident(incident_id):
    if request.method == 'POST':
        incident = Incident.query.get_or_404(incident_id)
        incident.status = 'Solved'
        db.session.commit()
        flash("Incident marked as resolved.", "success")
        return redirect(url_for('bp.incident_detail', incident_id=incident_id))

@bp.route('/incidents/<int:incident_id>/comment', methods=['POST'])
def comment_incident(incident_id):
   if request.method == 'POST':
        content=request.form['comment']
        if not content:
            flash("Comment cannot be empty!", "error")
            return redirect(url_for('bp.incident_detail', incident_id=incident_id))
        else:
            new_comment = Comment(content=content, incident_id=incident_id)
            db.session.add(new_comment)
            db.session.commit()
            flash("Comment added successfully!", "success")
            return redirect(url_for('bp.incident_detail', incident_id=incident_id))


'''
@bp.route('/health')
def health_check():
    return jsonify({'status': 'ok', 'message': 'service is up'}), 200
'''