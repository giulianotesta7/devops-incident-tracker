from flask import Blueprint, render_template, redirect, url_for, request, flash
from models import Incident
from database import db

bp = Blueprint('bp', __name__)

@bp.route('/')
def root():
    return redirect(url_for('bp.incidents'))

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/create-incident', methods=['GET', 'POST'])
def create_incident():
    if request.method == 'POST':
        tittle=request.form['title']
        description=request.form['description']
        severity=request.form['severity']
        if not tittle or not description or not severity:
            flash("All fields are required!", "error")
            return redirect(url_for('bp.create_incident'))
        else:
            new_incident = Incident(title=tittle, description=description, severity=severity)
            db.session.add(new_incident)
            db.session.commit()
            flash("Incident created successfully!", "success")
            return redirect(url_for('bp.create_incident'))
    


    return render_template('create-incident.html')

@bp.route('/incidents')
def incidents():
    incidents = Incident.query.order_by(Incident.created_at.desc()).all()
    return render_template('incidents.html', incidents=incidents)