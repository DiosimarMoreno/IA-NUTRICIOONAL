import json
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import dashboard_bp
from ..extensions import db
from ..decorators import role_required
from ..models import Evaluacion
from ..services import ejecutar_analisis

@dashboard_bp.route('/')
@login_required
@role_required('user')
def index():
    evaluaciones = Evaluacion.query.filter_by(usuario_id=current_user.id).order_by(Evaluacion.fecha_registro.desc()).all()
    return render_template('dashboard/index.html', evaluaciones=evaluaciones)

@dashboard_bp.route('/evaluar')
@login_required
@role_required('user')
def evaluacion():
    return render_template('dashboard/evaluacion.html')

@dashboard_bp.route('/evaluar', methods=['POST'])
@login_required
@role_required('user')
def evaluar_post():
    estatura = request.form.get('estatura', type=float)
    peso = request.form.get('peso', type=float)
    porcentaje_grasa = request.form.get('porcentaje_grasa', type=float)
    nivel_actividad = request.form.get('nivel_actividad', '').strip()
    objetivo_principal = request.form.get('objetivo_principal', '').strip()

    if not all([estatura, peso, nivel_actividad, objetivo_principal]):
        flash('Todos los campos obligatorios deben estar completos.', 'error')
        return redirect(url_for('dashboard.evaluacion'))

    datos = {
        "estatura": estatura,
        "peso": peso,
        "pc_grasa": porcentaje_grasa,
        "nivel_actividad": nivel_actividad,
        "objetivo": objetivo_principal,
        "edad": current_user.edad,
        "sexo": current_user.sexo,
    }

    resultados = ejecutar_analisis(datos)

    if "error" in resultados:
        flash(resultados["error"], "error")
        return redirect(url_for("dashboard.evaluacion"))

    ev = Evaluacion(
        usuario_id=current_user.id,
        estatura=estatura,
        peso=peso,
        porcentaje_grasa=porcentaje_grasa,
        nivel_actividad=nivel_actividad,
        objetivo_principal=objetivo_principal,
        resultados=json.dumps(resultados)
    )
    db.session.add(ev)
    db.session.commit()

    return redirect(url_for('dashboard.resultados', id=ev.id))

@dashboard_bp.route('/resultados/<int:id>')
@login_required
@role_required('user')
def resultados(id):
    ev = Evaluacion.query.get_or_404(id)
    if ev.usuario_id != current_user.id:
        return 'Acceso denegado', 403
    resultados_dict = json.loads(ev.resultados) if ev.resultados else {}
    return render_template('dashboard/resultados.html', evaluacion=ev, r=resultados_dict)

@dashboard_bp.route('/plan-accion/<int:id>')
@login_required
@role_required('user')
def plan_accion(id):
    ev = Evaluacion.query.get_or_404(id)
    if ev.usuario_id != current_user.id:
        return 'Acceso denegado', 403
    resultados_dict = json.loads(ev.resultados) if ev.resultados else {}
    return render_template('dashboard/plan_accion.html', evaluacion=ev, r=resultados_dict)