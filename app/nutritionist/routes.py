from flask import render_template, redirect, url_for, flash, request, Response
from flask_login import login_required, current_user
from . import nutritionist_bp
from ..decorators import role_required
from ..models import User, Evaluacion
from ..extensions import db
from ..services.pdf_report import generar_reporte_pdf

PACIENTES_POR_PAGINA = 20


def _obtener_riesgo_paciente(usuario_id: int) -> str:
    """Determina el nivel de riesgo más alto del paciente."""
    evaluaciones = Evaluacion.query.filter_by(usuario_id=usuario_id).all()
    niveles = {'Bajo': 0, 'Moderado': 1, 'Alto': 2}
    max_nivel = 'Bajo'
    for ev in evaluaciones:
        r = ev.resultados_dict
        meta = r.get('riesgo_metabolico', 'Bajo') or 'Bajo'
        nutri = r.get('riesgo_nutricional', 'Bajo') or 'Bajo'
        for nivel in (meta, nutri):
            if niveles.get(nivel, 0) > niveles.get(max_nivel, 0):
                max_nivel = nivel
    return max_nivel


def _enriquecer_paciente(p: User):
    """Añade datos calculados a un objeto paciente."""
    latest = Evaluacion.query.filter_by(usuario_id=p.id) \
        .order_by(Evaluacion.fecha_registro.desc()).first()
    riesgo = _obtener_riesgo_paciente(p.id) if latest else 'Bajo'
    return {
        'id': p.id,
        'nombre': p.nombre,
        'correo': p.correo,
        'edad': p.edad,
        'sexo': p.sexo,
        'fecha_registro': p.fecha_registro,
        'ultima_evaluacion': {
            'fecha': latest.fecha_registro.strftime('%d/%m/%Y'),
            'fecha_dmy': latest.fecha_registro.strftime('%Y-%m-%d'),
            'imc': latest.imc,
            'clasificacion': latest.clasificacion_imc,
        } if latest else None,
        'riesgo_meta': riesgo,
        'total_evaluaciones': Evaluacion.query.filter_by(usuario_id=p.id).count(),
    }


@nutritionist_bp.route('/')
@login_required
@role_required('nutritionist')
def index():
    pacientes_query = User.query.filter_by(role='user').order_by(User.fecha_registro.desc()).all()
    pacientes = [_enriquecer_paciente(p) for p in pacientes_query]

    total_evaluaciones = Evaluacion.query.count()
    pacientes_riesgo_alto = sum(
        1 for p in pacientes if p['riesgo_meta'] == 'Alto'
    )

    return render_template(
        'nutritionist/index.html',
        user=current_user,
        total_pacientes=len(pacientes),
        total_evaluaciones=total_evaluaciones,
        pacientes_riesgo_alto=pacientes_riesgo_alto,
        pacientes=pacientes,
    )


@nutritionist_bp.route('/patients')
@login_required
@role_required('nutritionist')
def patients():
    pagina = request.args.get('page', 1, type=int)
    if pagina < 1:
        pagina = 1

    query = User.query.filter_by(role='user').order_by(User.fecha_registro.desc())
    total = query.count()
    total_paginas = max(1, (total + PACIENTES_POR_PAGINA - 1) // PACIENTES_POR_PAGINA)
    if pagina > total_paginas:
        pagina = total_paginas

    pacientes_query = query.offset((pagina - 1) * PACIENTES_POR_PAGINA).limit(PACIENTES_POR_PAGINA).all()
    pacientes = [_enriquecer_paciente(p) for p in pacientes_query]

    return render_template(
        'nutritionist/patients.html',
        user=current_user,
        pacientes=pacientes,
        total_pacientes=total,
        pagina_actual=pagina,
        total_paginas=total_paginas,
    )


@nutritionist_bp.route('/patient/<int:id>')
@login_required
@role_required('nutritionist')
def patient_detail(id):
    paciente = User.query.get_or_404(id)

    if paciente.role != 'user':
        flash('El ID especificado no corresponde a un paciente.', 'error')
        return redirect(url_for('nutritionist.patients'))

    evaluaciones = Evaluacion.query \
        .filter_by(usuario_id=paciente.id) \
        .order_by(Evaluacion.fecha_registro.desc()) \
        .all()

    return render_template(
        'nutritionist/patient_detail.html',
        user=current_user,
        paciente=paciente,
        evaluaciones=evaluaciones,
    )


@nutritionist_bp.route('/descargar-reporte/<int:id>')
@login_required
@role_required('nutritionist')
def descargar_reporte(id):
    ev = Evaluacion.query.get_or_404(id)
    paciente = User.query.get_or_404(ev.usuario_id)

    if paciente.role != 'user':
        flash('Evaluacion no valida.', 'error')
        return redirect(url_for('nutritionist.patients'))

    pdf_bytes = generar_reporte_pdf(ev, paciente)
    nombre_limpio = paciente.nombre.replace(" ", "_")
    return Response(
        pdf_bytes,
        mimetype='application/pdf',
        headers={
            'Content-Disposition': f'attachment; filename=reporte_{nombre_limpio}_{ev.id}.pdf'
        }
    )
