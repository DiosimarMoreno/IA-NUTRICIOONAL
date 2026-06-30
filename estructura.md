# NutriExpert — Guía del Proyecto

## ¿Qué es?

Plataforma de evaluación nutricional con sistema experto clínico.
Calcula IMC, composición corporal, gasto energético y macronutrientes
de forma personalizada.

Dos tipos de usuario:
- **Usuario común** — realiza evaluaciones y ve su historial
- **Nutricionista** — panel con funciones adicionales para gestionar pacientes

---

## Tecnologías

| Capa | Tecnología |
|---|---|
| Backend | Python / Flask |
| Frontend | HTML + CSS + JavaScript vanilla |
| Base de datos | SQLite (SQLAlchemy ORM) |
| Plantillas | Jinja2 (server-side render) |
| Autenticación | Flask-Login (sesiones con cookies) |
| Contraseñas | werkzeug.security (pbkdf2:sha256) |

---

## Estructura del proyecto

```
IA-NUTRICIOONAL/
│
├── run.py                 # Punto de entrada: python run.py
├── requirements.txt       # Dependencias Python
├── .env                   # Variables de entorno (no subir a git)
├── .gitignore
│
├── app/                   # Código principal de Flask
│   ├── __init__.py        # Fábrica create_app() + comando init-db
│   ├── config.py          # Configuración desde .env
│   ├── extensions.py      # db, login_manager, migrate, csrf
│   ├── models.py          # Modelos: User, Evaluacion
│   │
│   ├── main/              # Blueprint público
│   │   ├── __init__.py
│   │   └── routes.py      # GET / → home.html (landing + login/register)
│   │
│   ├── auth/              # Blueprint de autenticación
│   │   ├── __init__.py
│   │   └── routes.py      # POST /auth/login, /auth/register, /auth/logout
│   │
│   ├── dashboard/         # Blueprint del usuario común
│   │   ├── __init__.py
│   │   └── routes.py      # /dashboard, /dashboard/evaluar,
│   │                      # /dashboard/resultados/<id>, /dashboard/plan-accion/<id>
│   │
│   ├── nutritionist/      # Blueprint del nutricionista
│   │   ├── __init__.py
│   │   └── routes.py      # /nutritionist, /nutritionist/patients
│   │
│   ├── services/          # Motor clínico (sistema experto)
│   │   ├── __init__.py              # ejecutar_analisis() — orquestador
│   │   ├── clinical_knowledge.py    # Fórmulas clínicas (IMC, Devine, Watson, etc.)
│   │   ├── nutritional_knowledge.py # Fórmulas nutricionales (TMB, macros, etc.)
│   │   ├── evaluation_schema.py     # Dataclass ResultadoEvaluacion
│   │   ├── inference_engine.py      # Motor forward-chaining
│   │   └── knowledge_base.py        # 40 reglas clínicas en 6 módulos
│   │
│   └── templates/         # Plantillas Jinja2
│       ├── main/
│       │   └── home.html            # Landing + login + register (3 vistas con JS)
│       ├── dashboard/
│       │   ├── index.html           # Panel del usuario (perfil + historial)
│       │   ├── evaluacion.html      # Formulario de 4 pasos
│       │   ├── resultados.html      # Informe completo de resultados
│       │   └── plan_accion.html     # Plan de acción personalizado
│       └── nutritionist/
│           ├── index.html           # Panel del nutricionista (placeholder)
│           └── patients.html        # Lista de pacientes (placeholder)
│
│   └── static/             # Archivos estáticos
│       ├── css/
│       │   ├── styles.css       # Estilos de la landing
│       │   ├── cuenta.css       # Estilos del panel de usuario
│       │   ├── evaluacion.css   # Estilos del formulario
│       │   ├── resultados.css   # Estilos del informe
│       │   └── plan_accion.css  # Estilos del plan de acción
│       ├── js/
│       │   ├── app.js           # Navegación entre vistas (landing/login/register)
│       │   └── evaluacion.js    # Validación en vivo del formulario
│       └── img/                 # Imágenes
│           ├── login_nombre.jpg
│           ├── campos.jpg
│           ├── entrenamiento.jpg
│           ├── evaluacion.jpg
│           ├── nutricion.jpg
│           ├── progreso.jpg
│           └── resultados.jpg
│
└── instance/              # Base de datos SQLite (se crea sola al iniciar)
    └── nutriexpert.db

```

---

## Cómo funciona

### Flujo del usuario

```
1. Landing (/) → El usuario ve la página principal
   └── Se registra o inicia sesión (tres vistas intercambiables con JS)

2. Dashboard (/dashboard) → Panel con perfil e historial de evaluaciones
   └── Botón "Nueva Evaluación" → formulario clínico

3. Evaluación (/dashboard/evaluar) → Formulario con 4 pasos:
   01. Datos personales (estatura, peso, edad, sexo)
   02. Composición corporal (% grasa, opcional)
   03. Nivel de actividad física
   04. Objetivo principal
   └── JS valida campos requeridos antes de habilitar el envío
   └── POST /dashboard/evaluar → procesa con motor clínico

4. Resultados (/dashboard/resultados/<id>) → Informe completo:
   - Parámetros introducidos
   - IMC + clasificación OMS
   - Peso ideal (Devine) + rango saludable
   - Somatotipo estimado
   - Masa grasa + masa magra
   - Agua corporal total (Watson)
   - TMB (Mifflin-St Jeor)
   - Gasto energético total (x factor actividad)
   - Calorías objetivo (según meta)
   - Distribución de macronutrientes (proteínas, carbohidratos, grasas)
   - Riesgo metabólico y nutricional
   - Nota clínica y recomendaciones
```

### Flujo del nutricionista

```
1. Login como nutritionist → /nutritionist
2. Ve panel con opciones
3. Puede ver lista de pacientes (próximamente)
```

---

## Blueprints (organización de rutas)

| Blueprint | Prefijo URL | ¿Qué hace? |
|---|---|---|
| `main` | `/` | Página principal (landing + login/register) |
| `auth` | `/auth` | Rutas de autenticación (login, register, logout) |
| `dashboard` | `/dashboard` | Panel del usuario común |
| `nutritionist` | `/nutritionist` | Panel del nutricionista |

Todas las rutas usan formularios HTML con POST y redireccionan.
No hay API JSON. La protección CSRF está activa globalmente.

---

## Base de datos (SQLAlchemy)

### Modelo `User` (tabla `usuarios`)

| Columna | Tipo | Detalle |
|---|---|---|
| id | Integer PK | |
| nombre | String(100) | |
| correo | String(100) | Único, usado para login |
| edad | Integer | |
| sexo | String(1) | M / F / O |
| contrasena_hash | String(255) | Hash (werkzeug.security) |
| fecha_registro | DateTime | |
| role | String(20) | 'user' por defecto, 'nutritionist' |

### Modelo `Evaluacion` (tabla `evaluaciones`)

| Columna | Tipo | Detalle |
|---|---|---|
| id | Integer PK | |
| usuario_id | Integer FK | Relacionado con User (cascade delete) |
| estatura | Float | cm |
| peso | Float | kg |
| porcentaje_grasa | Float | Opcional |
| nivel_actividad | String | sedentario / ligero / moderado / intenso / extremo |
| objetivo_principal | String | hipertrofia / mantenimiento / perdida |
| resultados | Text (JSON) | Output completo del motor clínico |
| fecha_registro | DateTime | |

---

## Servicios — Motor clínico (sistema experto)

`app/services/` implementa un sistema experto basado en reglas (forward-chaining):

| Archivo | Descripción |
|---|---|
| `knowledge_base.py` | 40 reglas clínicas con factores de certeza, organizadas en 6 módulos |
| `inference_engine.py` | Motor de inferencia que dispara reglas por etapas |
| `clinical_knowledge.py` | Fórmulas clínicas: IMC, Devine, Watson, Deurenberg, somatotipo |
| `nutritional_knowledge.py` | Fórmulas nutricionales: Mifflin-St Jeor, macros, actividad |
| `evaluation_schema.py` | Dataclass `ResultadoEvaluacion` con 26 campos calculados |
| `__init__.py` | `ejecutar_analisis(datos)` — orquesta el motor completo |

### Etapas del motor de inferencia

1. **validacion** — verifica datos de entrada
2. **antropometrico** — IMC, clasificación OMS, peso ideal, somatotipo, agua
3. **metabolico** — TMB, factor de actividad
4. **adaptacion** — calorías objetivo según meta
5. **prescripcion** — distribución de macronutrientes
6. **riesgos** — riesgo metabólico/nutricional, alertas, nota clínica

---

## Frontend

- **HTML** → Jinja2 templates en `app/templates/`
- **CSS** → Archivos separados en `static/css/` por sección
- **JS** → `app.js` (navegación entre vistas) y `evaluacion.js` (validación de formulario)
- **Imágenes** → `static/img/`

Las rutas HTML se cargan con `url_for('dashboard.index')` y los
archivos estáticos con `url_for('static', filename='css/...')`.

---

## Roles de usuario

| role | Acceso |
|---|---|
| `user` | `/dashboard/*` — evaluaciones y resultados propios |
| `nutritionist` | `/nutritionist/*` — panel de gestión (en desarrollo) |

El role se asigna al crear el usuario. Por defecto es `user`.

---

## Cómo ejecutar

```bash
# 1. Activar entorno virtual (Windows)
.\venv\Scripts\Activate.ps1

# Linux/macOS
source venv/bin/activate

# 2. Inicializar base de datos (solo la primera vez)
flask init-db

# 3. Ejecutar servidor
flask run --debug
```

Abrir `http://127.0.0.1:5000/` en el navegador.
