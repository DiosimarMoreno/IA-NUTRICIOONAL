import json
from datetime import datetime
from flask_login import UserMixin
from .extensions import db

class User(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    sexo = db.Column(db.String(1), nullable=False)
    contrasena_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    evaluaciones = db.relationship('Evaluacion', backref='usuario', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.nombre}>'


class Evaluacion(db.Model):
    __tablename__ = 'evaluaciones'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    estatura = db.Column(db.Float, nullable=False)
    peso = db.Column(db.Float, nullable=False)
    porcentaje_grasa = db.Column(db.Float, nullable=True)
    nivel_actividad = db.Column(db.String(50), nullable=False)
    objetivo_principal = db.Column(db.String(50), nullable=False)
    resultados = db.Column(db.Text, nullable=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def resultados_dict(self):
        if self.resultados:
            return json.loads(self.resultados)
        return {}

    @property
    def imc(self):
        return self.resultados_dict.get('imc', '')

    @property
    def clasificacion_imc(self):
        return self.resultados_dict.get('clasificacion_imc', '')

    def __repr__(self):
        return f'<Evaluacion {self.id} usuario={self.usuario_id}>'