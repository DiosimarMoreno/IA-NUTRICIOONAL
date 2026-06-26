from flask import render_template
from flask_login import login_required, current_user
from . import nutritionist_bp

@nutritionist_bp.route('/')
@login_required
def index():
    # Solo nutricionistas
    return render_template('nutritionist/index.html', user=current_user)

@nutritionist_bp.route('/patients')
@login_required
def patients():
    return render_template('nutritionist/patients.html')