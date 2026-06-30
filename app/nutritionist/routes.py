from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from . import nutritionist_bp
from ..decorators import role_required

@nutritionist_bp.route('/')
@login_required
@role_required('nutritionist')
def index():
    # Solo nutricionistas
    return render_template('nutritionist/index.html', user=current_user)

@nutritionist_bp.route('/patients')
@login_required
@role_required('nutritionist')
def patients():
    return render_template('nutritionist/patients.html')