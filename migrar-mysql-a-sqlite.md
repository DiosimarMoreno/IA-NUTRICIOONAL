# Migración de MySQL a SQLite

## Esquema original (MySQL)

### Tabla: `usuarios`

```sql
CREATE TABLE `usuarios` (
  `id`              INT(11)      NOT NULL AUTO_INCREMENT,
  `nombre`          VARCHAR(100) NOT NULL,
  `correo`          VARCHAR(100) NOT NULL UNIQUE,
  `edad`            INT(11)      NOT NULL,
  `sexo`            CHAR(1)      NOT NULL,       -- 'M', 'F' u 'O'
  `contrasena`      VARCHAR(255) NOT NULL,        -- texto plano
  `fecha_registro`  TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);
```

### Tabla: `evaluaciones`

```sql
CREATE TABLE `evaluaciones` (
  `id_evaluacion`    INT(11)      NOT NULL AUTO_INCREMENT,
  `id_usuario`       INT(11)      NOT NULL,
  `estatura`         DECIMAL(5,2) NOT NULL,       -- en cm
  `peso`             DECIMAL(5,2) NOT NULL,       -- en kg
  `porcentaje_grasa` DECIMAL(4,1) DEFAULT NULL,   -- opcional
  `nivel_actividad`  VARCHAR(50)  NOT NULL,
  `objetivo_principal` VARCHAR(50) NOT NULL,
  `fecha_registro`   TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_evaluacion`),
  FOREIGN KEY (`id_usuario`) REFERENCES `usuarios`(`id`) ON DELETE CASCADE
);
```

### Dato existente

```sql
-- 1 usuario registrado:
INSERT INTO `usuarios` VALUES (
  1,
  'Diosimar Moreno',
  'morenodiosimar@gmail.com',
  21,
  'F',
  'Reina12**',   -- ⚠ texto plano, habrá que hashear con bcrypt
  '2026-06-17 22:06:42'
);

-- evaluaciones: vacío (no hay registros)
```

---

## Equivalente en SQLAlchemy (SQLite)

```python
# app/models.py

class User(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id            = db.Column(db.Integer, primary_key=True)
    nombre        = db.Column(db.String(100), nullable=False)
    correo        = db.Column(db.String(100), unique=True, nullable=False)
    edad          = db.Column(db.Integer, nullable=False)
    sexo          = db.Column(db.String(1), nullable=False)
    contrasena_hash = db.Column(db.String(255), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    evaluaciones = db.relationship('Evaluacion', backref='usuario', cascade='all, delete-orphan')


class Evaluacion(db.Model):
    __tablename__ = 'evaluaciones'

    id                = db.Column(db.Integer, primary_key=True)
    usuario_id        = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    estatura          = db.Column(db.Float, nullable=False)
    peso              = db.Column(db.Float, nullable=False)
    porcentaje_grasa  = db.Column(db.Float, nullable=True)
    nivel_actividad   = db.Column(db.String(50), nullable=False)
    objetivo_principal = db.Column(db.String(50), nullable=False)
    resultados        = db.Column(db.Text, nullable=True)       # JSON string
    fecha_registro    = db.Column(db.DateTime, default=datetime.utcnow)
```

**Cambios respecto a MySQL:**
| MySQL | SQLite / SQLAlchemy |
|---|---|
| `contrasena` (texto plano) | `contrasena_hash` (bcrypt) |
| `DECIMAL(5,2)` | `Float` |
| `id_evaluacion` | `id` |
| `id_usuario` FK | `usuario_id` FK |
| — | `resultados` (nuevo, JSON) |

---

## Script de migración (para cuando lo necesites)

Crea `scripts/migrar.py`:

```python
"""Migra datos de MySQL a SQLite, hasheando contraseñas con bcrypt."""

import sqlite3
import bcrypt

# 1. Conectar a MySQL y leer datos
# (requiere mysql-connector-python o pymysql)
#
# import mysql.connector
# mysql_conn = mysql.connector.connect(
#     host='localhost', user='root', password='', database='nutriexpert'
# )
# cursor = mysql_conn.cursor(dictionary=True)
# cursor.execute("SELECT * FROM usuarios")
# usuarios = cursor.fetchall()

# 2. Conectar a SQLite (la misma DB que usa Flask)
sqlite_conn = sqlite3.connect('instance/nutriexpert.db')
cursor = sqlite_conn.cursor()

# 3. Insertar cada usuario con contraseña hasheada
# for u in usuarios:
#     hash_pw = bcrypt.hashpw(u['contrasena'].encode(), bcrypt.gensalt())
#     cursor.execute(
#         "INSERT INTO usuarios (nombre, correo, edad, sexo, contrasena_hash, fecha_registro) "
#         "VALUES (?, ?, ?, ?, ?, ?)",
#         (u['nombre'], u['correo'], u['edad'], u['sexo'], hash_pw.decode(), u['fecha_registro'])
#     )

sqlite_conn.commit()
sqlite_conn.close()
print("Migración completada.")
```

> **Nota:** El script está comentado porque requiere `mysql-connector-python`. No lo necesitas ahora — se ejecutará cuando tengas datos en MySQL que migrar.
