from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import auth_bp
from ..extensions import db
from ..models import User

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'nutritionist':
            return redirect(url_for('nutritionist.index'))
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        correo = request.form.get('correo', '').strip()
        contrasena = request.form.get('contrasena', '')

        if not correo or not contrasena:
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('main.home'))

        usuario = User.query.filter_by(correo=correo).first()

        if not usuario or not check_password_hash(usuario.contrasena_hash, contrasena):
            flash('Correo o contraseña incorrectos.', 'error')
            return redirect(url_for('main.home'))

        login_user(usuario)
        flash(f'¡Bienvenido de nuevo, {usuario.nombre}!', 'success')

        if usuario.role == 'nutritionist':
            return redirect(url_for('nutritionist.index'))
        return redirect(url_for('dashboard.index'))

    return redirect(url_for('main.home'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        if current_user.role == 'nutritionist':
            return redirect(url_for('nutritionist.index'))
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        correo = request.form.get('correo', '').strip()
        edad = request.form.get('edad', '').strip()
        sexo = request.form.get('sexo', '').strip()
        contrasena = request.form.get('contrasena', '')

        if not all([nombre, correo, edad, sexo, contrasena]):
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('main.home'))

        if User.query.filter_by(correo=correo).first():
            flash('El correo ya está registrado.', 'error')
            return redirect(url_for('main.home'))

        role = request.form.get('role', 'user').strip()
        if role not in ('user', 'nutritionist'):
            role = 'user'

        usuario = User(
            nombre=nombre,
            correo=correo,
            edad=int(edad),
            sexo=sexo.upper(),
            contrasena_hash=generate_password_hash(contrasena),
            role=role
        )
        db.session.add(usuario)
        db.session.commit()

        flash('¡Cuenta creada con éxito! Ahora inicia sesión.', 'success')
        return redirect(url_for('main.home'))

    return redirect(url_for('main.home'))

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'success')
    return redirect(url_for('main.home'))