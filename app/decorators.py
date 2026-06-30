from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role != role:
                flash('Acceso denegado. No tienes permisos para esta sección.', 'error')
                if current_user.role == 'nutritionist':
                    return redirect(url_for('nutritionist.index'))
                return redirect(url_for('dashboard.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
