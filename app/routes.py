from flask import Blueprint, render_template

bp = Blueprint('bp', __name__)

@bp.route('/about')
def index():
    return render_template('about.html')

#@bp.route('/create_incident')
#def incident():
#    return render_template('incident.html')

