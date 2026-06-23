# ROADMAP: Migración a Flask + SQLite + JWT

## Estado actual

- **Frontend:** HTML/CSS/JS vanilla — funcional, diseño moderno terminado
- **Backend:** Node.js + Express + MySQL — funcional pero inseguro (contraseñas en texto plano)
- **Motor clínico:** No existe — el botón "Ejecutar Análisis" solo redirige a resultados.html sin enviar datos
- **Página de resultados:** Muestra placeholders (0.0, 0%, etc.) — ningún cálculo se ejecuta
- **package.json:** Contiene ~100 dependencias de React/Vite/Tailwind que no se usan

## Meta final

Backend en Flask (Python) con SQLite, autenticación JWT, y un motor de inferencia clínica que calcule IMC, TMB, macronutrientes, somatotipo, etc. El frontend HTML/CSS/JS se conserva intacto — solo se modifica `scripts.js`.

---

## Fase 0 — Preparación del proyecto

### 0.1 Crear estructura de carpetas

Estructura profesional con backend (Flask) y frontend separados por carpeta raíz:

```
IA-NUTRICIOONAL/
├── backend/                          # Flask API
│   ├── app.py                        # Entry point, app factory
│   ├── config.py                     # Config clases (dev/prod)
│   ├── models.py                     # SQLAlchemy ORM
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py                   # /api/auth/register, /api/auth/login
│   │   └── evaluations.py            # /api/evaluations CRUD
│   ├── services/
│   │   ├── __init__.py
│   │   ├── clinical.py               # IMC, somatotipo, composición corporal
│   │   └── nutrition.py              # TMB, macros, calorías objetivo
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── auth.py                   # Decorador @jwt_required
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── evaluation.py             # Validación con dataclasses o marshmallow
│   ├── utils/
│   │   ├── __init__.py
│   │   └── validators.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py               # Fixtures (test client, test DB)
│   │   ├── test_auth.py
│   │   ├── test_evaluations.py
│   │   └── test_clinical.py
│   ├── requirements.txt
│   └── .env
├── frontend/                         # Static frontend (sin build tool)
│   ├── index.html                    # Landing + login/register
│   ├── dashboard.html                # Panel de control (antes cuenta.html)
│   ├── evaluation.html               # Formulario clínico
│   ├── results.html                  # Informe de resultados
│   ├── css/
│   │   ├── main.css                  # Estilos globales (antes styles.css)
│   │   ├── dashboard.css             # (antes cuenta.css)
│   │   ├── evaluation.css
│   │   └── results.css
│   ├── js/
│   │   ├── api.js                    # Cliente fetch con base URL y JWT
│   │   ├── auth.js                   # Login, registro, logout
│   │   ├── dashboard.js              # Historial y cards del dashboard
│   │   ├── evaluation.js             # Validación y envío del formulario
│   │   ├── results.js                # Poblar resultados en el DOM
│   │   └── utils.js                  # Formateadores y helpers
│   └── img/
│       ├── login_nombre.jpg
│       ├── entrenamiento.jpg
│       ├── evaluacion.jpg
│       ├── nutricion.jpg
│       ├── progreso.jpg
│       └── resultados.jpg
├── scripts/                          # Scripts auxiliares
│   ├── migrate_mysql_to_sqlite.py
│   └── seed.py                       # Datos de demostración
├── .gitignore
├── .env.example
├── README.md
└── ROADMAP.md
```

> **Nota sobre nombres:** Los archivos del frontend pueden renombrarse a español si se prefiere (`panel.html`, `evaluacion.html`, `resultados.html`), o mantenerse en inglés. Lo importante es la separación de carpetas y la organización por capas.

### 0.2 Crear y activar entorno virtual

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 0.3 Instalar dependencias

Crear `requirements.txt`:

```
flask==3.1.*
flask-cors==5.*
flask-sqlalchemy==3.*
pyjwt==2.*
bcrypt==4.*
python-dotenv==1.*
```

Instalar:

```bash
pip install -r requirements.txt
```

### 0.4 Crear `.env`

```
SECRET_KEY=genera-una-clave-segura-aqui
DATABASE_URL=sqlite:///nutriexpert.db
```

### 0.6 Actualizar rutas de CSS y JS en los HTML

Al mover los archivos a `frontend/`, `frontend/css/` y `frontend/js/`, las rutas relativas en los HTML quedaron rotas. Hay que corregir **12 referencias** en total.

**Regla general:**
- CSS cambia de `nombre.css` → `css/nombre.css`
- `scripts.js` cambia de `scripts.js` → `../scripts.js` (porque está en la raíz del proyecto)

**Cambios necesarios en cada archivo:**

#### `frontend/index.html`
| Línea | Ruta actual | Ruta correcta |
|---|---|---|
| 7 | `<link rel="stylesheet" href="styles.css">` | `<link rel="stylesheet" href="css/styles.css">` |
| 245 | `<script src="scripts.js"></script>` | `<script src="../scripts.js"></script>` |

#### `frontend/cuenta.html`
| Línea | Ruta actual | Ruta correcta |
|---|---|---|
| 7 | `<link rel="stylesheet" href="cuenta.css">` | `<link rel="stylesheet" href="css/cuenta.css">` |
| 112 | `<script src="scripts.js"></script>` | `<script src="../scripts.js"></script>` |

#### `frontend/evaluacion.html`
| Línea | Ruta actual | Ruta correcta |
|---|---|---|
| 7 | `<link rel="stylesheet" href="evaluacion.css">` | `<link rel="stylesheet" href="css/evaluacion.css">` |
| 194 | `<script src="scripts.js"></script>` | `<script src="../scripts.js"></script>` |

#### `frontend/resultados.html`
| Línea | Ruta actual | Ruta correcta |
|---|---|---|
| 7 | `<link rel="stylesheet" href="resultados.css">` | `<link rel="stylesheet" href="css/resultados.css">` |
| 212 | `<script src="scripts.js"></script>` | `<script src="../scripts.js"></script>` |

> Las rutas de imágenes (`img/`) **no necesitan cambiar** porque los HTML y la carpeta `img/` están al mismo nivel dentro de `frontend/`.

---

### ⚠️ 0.5 Limpieza manual de package.json

El archivo `package.json` actual tiene ~100 dependencias que **no se usan en el frontend** (React, Framer Motion, Recharts, Tailwind, Vite, etc.). Como el frontend es HTML/CSS/JS vanilla, esas dependencias son lastre.

**Qué hacer:** Editar `package.json` y eliminar TODAS las dependencias de `"dependencies"`. Dejar solo lo mínimo si quieres conservar el servidor Express como respaldo:

```json
"dependencies": {
  "express": "^5.2.1",
  "mysql2": "^3.22.5",
  "cors": "^2.8.6"
}
```

Luego ejecutar `npm install` para regenerar `package-lock.json` y `node_modules/` limpio.

**Dependencias a eliminar (lista completa):**
- react, react-dom, react-router, react-hook-form, react-dnd, react-day-picker, react-slick, react-smooth, react-transition-group, react-fast-compare, react-is, react-popper, react-refresh, react-remove-scroll, react-remove-scroll-bar, react-resizable-panels, react-responsive-masonry, react-style-singleton
- framer-motion, motion, motion-dom, motion-utils
- recharts, recharts-scale, victory-vendor, d3-*, decimal.js-light
- tailwindcss, tailwind-merge, tw-animate-css, postcss, lightningcss
- vite, esbuild, rollup, enhanced-resolve
- lucide-react, cmdk, vaul, sonner, input-otp, embla-carousel*, next-themes
- class-variance-authority, clsx, classnames
- cosmiconfig, babel-*, caniuse-lite, browserslist, electron-to-chromium
- aria-hidden, detect-node-es, get-nonce, use-callback-ref, use-sidecar
- nanoid, picocolors, picomatch, tinyglobby, fdir
- date-fns, lodash, lodash.debounce
- prop-types, hoist-non-react-statics, warning
- @formatjs/icu-messageformat-parser, @formatjs/intl-localematcher (si aparecen)

### 0.6 Actualizar `.gitignore`

```gitignore
node_modules/
venv/
*.db
.env
__pycache__/
```

---

## Fase 1 — Base de datos y modelos

### 1.1 Crear `config.py`

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///nutriexpert.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### 1.2 Crear `models.py`

Definir dos modelos con SQLAlchemy:

**Usuario**
| Columna | Tipo | Detalle |
|---|---|---|
| id | Integer, PK, autoincrement | |
| nombre | String(100), NOT NULL | Nombre completo |
| correo | String(100), UNIQUE, NOT NULL | Email de inicio de sesión |
| edad | Integer, NOT NULL | Edad en años |
| sexo | String(1), NOT NULL | 'M', 'F' u 'O' |
| contrasena_hash | String(255), NOT NULL | Hash de bcrypt (no texto plano) |
| fecha_registro | DateTime, default=now | |

**Evaluacion**
| Columna | Tipo | Detalle |
|---|---|---|
| id | Integer, PK, autoincrement | |
| usuario_id | Integer, FK -> usuario.id, NOT NULL | Con CASCADE al borrar usuario |
| estatura | Float, NOT NULL | Altura en cm |
| peso | Float, NOT NULL | Peso en kg |
| porcentaje_grasa | Float, nullable | % grasa corporal (opcional) |
| nivel_actividad | String(50), NOT NULL | sedentario / ligera / moderado / muy_activo / extremo |
| objetivo_principal | String(50), NOT NULL | hipertrofia / mantenimiento / perdida |
| resultados | Text (JSON), nullable | Aquí se guarda todo el output del motor de inferencia |
| fecha_registro | DateTime, default=now | |

### 1.3 Inicializar la base de datos

Agregar un comando a `app.py`:

```python
@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("Base de datos inicializada.")
```

Ejecutar:

```bash
flask init-db
```

Esto crea `instance/nutriexpert.db`.

---

## Fase 2 — Autenticación con JWT

### 2.1 Crear `routes/auth.py`

Blueprint `auth` con dos rutas:

**POST /api/registrar**

- Recibe JSON: `{ nombre, correo, edad, sexo, contrasena }`
- Validar que todos los campos existan
- Verificar que el correo no esté registrado
- Hash de contraseña con `bcrypt.hashpw()`
- Guardar usuario
- Responder: `{ status: "success", message: "..." }`

**POST /api/login**

- Recibe JSON: `{ correo, contrasena }`
- Buscar usuario por correo
- Verificar contraseña con `bcrypt.checkpw()`
- Generar JWT con `pyjwt`: `{ "id": usuario.id, "nombre": usuario.nombre, "correo": usuario.correo, "exp": time + 86400 }`
- Responder: `{ status: "success", token: "<jwt>", usuario: { id, nombre, correo } }`

### 2.2 Crear decorador `@jwt_required`

En `routes/auth.py` o un archivo `routes/decorators.py`:

```python
from functools import wraps
import jwt
from flask import request, jsonify, current_app

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return jsonify(status="error", message="Token requerido"), 401
        try:
            payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            request.usuario = payload
        except jwt.ExpiredSignatureError:
            return jsonify(status="error", message="Token expirado"), 401
        except jwt.InvalidTokenError:
            return jsonify(status="error", message="Token inválido"), 401
        return f(*args, **kwargs)
    return decorated
```

### 2.3 Registrar el blueprint en `app.py`

```python
from routes.auth import auth_bp
app.register_blueprint(auth_bp)
```

### 2.4 Probar los endpoints

```bash
# Registrar
curl -X POST http://localhost:5000/api/registrar \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Test","correo":"test@test.com","edad":25,"sexo":"M","contrasena":"123456"}'

# Login
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"correo":"test@test.com","contrasena":"123456"}'
```

---

## Fase 3 — Motor de inferencia clínica

Este es el núcleo del sistema. Todas las funciones reciben datos y devuelven resultados sin tocar la base de datos.

### 3.1 Crear `services/calculos.py`

Funciones a implementar:

| Función | Fórmula | Fuente |
|---|---|---|
| `calcular_imc(peso_kg, altura_cm)` | `peso / (altura/100)^2` | — |
| `clasificar_imc(imc)` | <18.5→Bajo peso, 18.5-24.9→Normal, 25-29.9→Sobrepeso, 30-34.9→Obesidad I, 35-39.9→Obesidad II, >=40→Obesidad III | OMS |
| `peso_ideal_devine(altura_cm, sexo)` | Hombre: `50 + 0.9 * (altura - 152)` / Mujer: `45.5 + 0.9 * (altura - 152)` | Devine |
| `rango_saludable(altura_cm)` | Min: `18.5 * (altura/100)^2` / Max: `24.9 * (altura/100)^2` | OMS |
| `somatotipo_estimado(imc, grasa)` | Si grasa > 25% → Endomorfo, si IMC > 25 y grasa < 20% → Mesomorfo, si IMC < 20 → Ectomorfo | Estimación simple |
| `masa_grasa(peso_kg, pct_grasa)` | `peso * (pct_grasa / 100)` | — |
| `masa_magra(peso_kg, masa_grasa_kg)` | `peso - masa_grasa` | — |
| `agua_watson(peso_kg, altura_cm, edad, sexo)` | Hombre: `2.447 - (0.09156*edad) + (0.1074*altura) + (0.3362*peso)` / Mujer: `-2.097 + (0.1069*altura) + (0.2466*peso)` | Watson |

### 3.2 Crear `services/energia.py`

**TMB — Mifflin-St Jeor (recomendada por la ADA):**

- Hombre: `(10 * peso) + (6.25 * altura) - (5 * edad) + 5`
- Mujer: `(10 * peso) + (6.25 * altura) - (5 * edad) - 161`

**Factores de actividad:**

| Valor del formulario | Etiqueta | Factor PAL |
|---|---|---|
| `sedentario` | Sin ejercicio, trabajo de oficina | 1.2 |
| `ligera` | 1–3 días/semana | 1.375 |
| `moderado` | 3–5 días/semana | 1.55 |
| `muy_activo` | 6–7 días intenso | 1.725 |
| `extremo` | Dobles sesiones | 1.9 |

**Ajuste por objetivo:**

| Valor del formulario | Etiqueta | Multiplicador |
|---|---|---|
| `hipertrofia` | Ganar masa y fuerza | 1.15 (superávit) |
| `mantenimiento` | Preservar composición | 1.0 (mantenimiento) |
| `perdida` | Reducir % grasa | 0.80 (déficit) |

**Calorías objetivo:** `TMB * factor_actividad * factor_objetivo`

**Distribución de macronutrientes:**

| Objetivo | Proteína | Carbohidratos | Grasa |
|---|---|---|---|
| Hipertrofia | 2.0 g/kg peso | 4.0 g/kg peso | 0.8 g/kg peso |
| Mantenimiento | 1.6 g/kg peso | 3.0 g/kg peso | 0.8 g/kg peso |
| Pérdida de grasa | 2.2 g/kg peso | 2.5 g/kg peso | 0.7 g/kg peso |

**Calorías por gramo:** Proteína = 4 kcal/g, Carbohidratos = 4 kcal/g, Grasa = 9 kcal/g.

### 3.3 Función orquestadora

Crear una función `ejecutar_analisis(datos)` en `services/calculos.py` o `services/energia.py` que reciba:

```python
{
    "estatura": 175,
    "peso": 70,
    "porcentaje_grasa": 15.0,  # opcional
    "nivel_actividad": "moderado",
    "objetivo_principal": "hipertrofia",
    "edad": 25,
    "sexo": "M"
}
```

Y devuelva un diccionario completo con TODOS los resultados que necesita `resultados.html` (los 23 elementos DOM). Este diccionario es lo que se guarda en la columna `resultados` de la tabla `Evaluacion`.

### 3.4 Tests unitarios (opcional pero recomendado)

```bash
pip install pytest
```

Crear `services/test_calculos.py`:

```python
from calculos import calcular_imc, clasificar_imc, tmb_mifflin

def test_imc_normal():
    assert calcular_imc(70, 175) == 22.86  # redondeado

def test_clasificacion_normal():
    assert clasificar_imc(22.0) == "Normal"

def test_tmb_hombre():
    assert tmb_mifflin(70, 175, 25, "M") == 1665  # redondeado
```

```bash
pytest services/test_calculos.py -v
```

---

## Fase 4 — Endpoints de evaluación

### 4.1 Crear `routes/evaluaciones.py`

Blueprint `evaluaciones` (requiere JWT en todas las rutas).

**POST /api/evaluaciones**

- Requiere autenticación JWT
- Recibe: `{ estatura, peso, porcentaje_grasa (opcional), nivel_actividad, objetivo_principal }`
- Validar campos obligatorios
- Obtener edad y sexo desde el registro del usuario (usando `usuario_id` del token)
- Ejecutar `ejecutar_analisis()` con todos los datos
- Guardar `Evaluacion` con resultados en JSON
- Responder: `{ status: "success", evaluacion: { id, ...campos..., resultados: {...} } }`

**GET /api/evaluaciones**

- Lista evaluaciones del usuario autenticado
- Responder: `{ status: "success", evaluaciones: [ { id, fecha, imc, objetivo }, ... ] }`

**GET /api/evaluaciones/<id>**

- Evaluación específica (verificar que pertenezca al usuario)
- Responder: `{ status: "success", evaluacion: { ...todos los campos con resultados... } }`

### 4.2 Registrar el blueprint

```python
from routes.evaluaciones import evaluaciones_bp
app.register_blueprint(evaluaciones_bp)
```

---

## Fase 5 — Conectar el frontend

Esta es la única fase que toca archivos del frontend. Solo se modifica `scripts.js`.

### 5.1 Configurar la URL base

Al inicio de `scripts.js`, definir:

```javascript
const API_URL = "http://localhost:5000/api";
```

### 5.2 Actualizar login (scripts.js)

En el submit de `#form-login`:

- Cambiar endpoint a `${API_URL}/login`
- Guardar `resultado.token` en `localStorage.setItem("token", resultado.token)`
- Seguir guardando `resultado.usuario` como antes
- En los headers del fetch, agregar `"Authorization": "Bearer " + token`

### 5.3 Actualizar registro (scripts.js)

- Cambiar endpoint a `${API_URL}/registrar`
- No requiere token
- Igual que antes: mostrar mensaje y redirigir a login

### 5.4 Conectar el botón "Ejecutar Análisis Clínico"

Actualmente en `scripts.js` líneas 192-197:

```javascript
btnSubmit.addEventListener("click", (e) => {
    e.preventDefault();
    window.location.href = "resultados.html";
});
```

**Cambiar a:**

1. Leer valores del formulario: `estatura`, `peso`, `grasa-corporal`, `nivel_actividad`, `objetivo_principal`
2. Hacer fetch POST a `${API_URL}/evaluaciones` con `Authorization: Bearer <token>`
3. Si la respuesta es exitosa: guardar los resultados en `localStorage.setItem("resultados_nutriexpert", JSON.stringify(data.evaluacion))`
4. Redirigir a `resultados.html`
5. Si hay error: mostrar mensaje al usuario

### 5.5 Poblar la página de resultados (scripts.js)

`resultados.html` tiene 23 elementos DOM que esperan datos. En `scripts.js`, al cargar la página:

1. Leer `localStorage.getItem("resultados_nutriexpert")`
2. Si no hay datos, mostrar mensaje "No hay evaluación disponible"
3. Si hay datos, poblar cada elemento:

```javascript
// Bloque 1: Parámetros introducidos
document.getElementById("param-estatura").textContent = `${data.estatura} cm`;
document.getElementById("param-peso").textContent = `${data.peso} kg`;
document.getElementById("param-grasa").textContent = `${data.porcentaje_grasa || "—"}%`;
document.getElementById("param-actividad").textContent = data.resultados.actividad_etiqueta;
document.getElementById("param-objetivo").textContent = data.resultados.objetivo_etiqueta;

// Bloque 2: Antropométricas
document.getElementById("res-imc").textContent = data.resultados.imc;
document.getElementById("res-imc-estado").textContent = data.resultados.clasificacion_imc;
document.getElementById("res-peso-ideal").textContent = `${data.resultados.peso_ideal} kg`;
document.getElementById("res-peso-rango").textContent = `Rango Saludable: ${data.resultados.rango_min}kg - ${data.resultados.rango_max}kg`;
document.getElementById("res-somatotipo").textContent = data.resultados.somatotipo;
document.getElementById("res-somatotipo-desc").textContent = data.resultados.somatotipo_desc;
document.getElementById("res-grasa-masa").textContent = `${data.resultados.masa_grasa} kg`;
document.getElementById("res-masa-magra").textContent = `${data.resultados.masa_magra} kg`;
document.getElementById("res-agua-corporal").textContent = `${data.resultados.agua_corporal} L`;

// Bloque 3: Energía y macros
document.getElementById("res-tmb").innerHTML = `${data.resultados.tmb} <span class="unidad-cal">kcal</span>`;
document.getElementById("res-calorias-objetivo").innerHTML = `${data.resultados.calorias_objetivo} <span class="unidad-cal">kcal</span>`;
document.getElementById("pct-proteina").textContent = `${data.resultados.pct_proteina}%`;
document.getElementById("macro-proteina").textContent = `${data.resultados.proteina_g}g`;
document.getElementById("cal-proteina").textContent = `${data.resultados.cal_proteina} kcal aportadas`;
document.getElementById("pct-carbos").textContent = `${data.resultados.pct_carbos}%`;
document.getElementById("macro-carbos").textContent = `${data.resultados.carbos_g}g`;
document.getElementById("cal-carbos").textContent = `${data.resultados.cal_carbos} kcal aportadas`;
document.getElementById("pct-grasas").textContent = `${data.resultados.pct_grasas}%`;
document.getElementById("macro-grasas").textContent = `${data.resultados.grasas_g}g`;
document.getElementById("cal-grasas").textContent = `${data.resultados.cal_grasas} kcal aportadas`;
```

### 5.6 Cargar historial en cuenta.html

En `cuenta.html`, reemplazar el estado "vacío" con datos reales:

- Fetch GET a `${API_URL}/evaluaciones` con token
- Si hay evaluaciones: generar HTML dinámico con cada evaluación (fecha, IMC, objetivo)
- Cada evaluación debe linkear a `resultados.html?id=X` (pasar ID por URL)
- En `resultados.html`, si hay `?id=X` en la URL, hacer fetch GET a `${API_URL}/evaluaciones/X` en lugar de leer de localStorage

### 5.7 Actualizar cerrar sesión

```javascript
btnCerrarSesion.addEventListener("click", () => {
    localStorage.removeItem("token");
    localStorage.removeItem("usuario_nutriexpert");
    localStorage.removeItem("resultados_nutriexpert");
    window.location.href = "index.html";
});
```

---

## Fase 6 — Seguridad y robustez

### 6.1 Validación de entradas en backend

Crear una función `validar_evaluacion(datos)` que verifique:

- `estatura`: número entre 50 y 250 cm
- `peso`: número entre 10 y 400 kg
- `porcentaje_grasa`: número entre 3 y 60 (si se envía)
- `nivel_actividad`: uno de `["sedentario", "ligera", "moderado", "muy_activo", "extremo"]`
- `objetivo_principal`: uno de `["hipertrofia", "mantenimiento", "perdida"]`

Devolver error 400 si algo falla.

### 6.2 Manejadores de error globales

En `app.py`:

```python
@app.errorhandler(400)
def bad_request(e):
    return jsonify(status="error", message=str(e)), 400

@app.errorhandler(401)
def unauthorized(e):
    return jsonify(status="error", message="No autorizado"), 401

@app.errorhandler(404)
def not_found(e):
    return jsonify(status="error", message="Recurso no encontrado"), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify(status="error", message="Error interno del servidor"), 500
```

### 6.3 CORS

```python
from flask_cors import CORS

CORS(app, origins=["http://localhost:3000", "http://localhost:5500", "http://127.0.0.1:5500"])
```

### 6.4 Logging

```python
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
```

---

## Fase 7 — Scripts útiles

### 7.1 Migrar datos de MySQL a SQLite

Crear `scripts/migrar_mysql_a_sqlite.py`:

1. Conectar a MySQL con `mysql.connector` o `pymysql`
2. Leer todos los usuarios y evaluaciones
3. Conectar a SQLite
4. Insertar los datos (generar hash de contraseñas con bcrypt)
5. Verificar que las cuentas migradas funcionan con login

### 7.2 Respaldo de SQLite

```python
# scripts/backup_db.py
import shutil
shutil.copy("instance/nutriexpert.db", f"backups/nutriexpert_{datetime.now().strftime('%Y%m%d')}.db")
```

---

## Orden de ejecución resumido para el dev

```
Fase 0 ── Preparar carpetas, venv, requirements.txt, .env, .gitignore
    ↓
Fase 1 ── models.py, config.py, init-db
    ↓
Fase 2 ── routes/auth.py: registrar + login + JWT
    ↓
Fase 3 ── services/calculos.py + services/energia.py: el motor clínico
    ↓
Fase 4 ── routes/evaluaciones.py: endpoints de evaluación
    ↓
Fase 5 ── Modificar scripts.js: conectar frontend con Flask
    ↓
Fase 6 ── Validación, errores, CORS, logging
    ↓
Fase 7 ── Scripts de migración y respaldo
```

Cada fase depende de la anterior. No saltarse ninguna.

---

## Notas importantes

- **No modificar los archivos HTML ni CSS.** Todo el cambio frontend se hace exclusivamente en `scripts.js`.
- **El servidor Flask corre en `http://localhost:5000`** por defecto.
- **Las contraseñas van con bcrypt, nunca en texto plano.**
- **El JWT expira en 24 horas.** El frontend debe redirigir al login si recibe 401.
- **SQLite guarda el archivo en `instance/nutriexpert.db`** — agregar a `.gitignore`.
- **Usar `flask run --debug`** para recarga automática en desarrollo.
- **Campos.jpg** en `img/` no se referencia en ningún HTML — se puede eliminar manualmente.
