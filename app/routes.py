from flask import Blueprint, render_template

bp = Blueprint('bp', __name__)

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/create-incident', methods=['GET', 'POST'])
def create_incident():
    return render_template('create-incident.html')

