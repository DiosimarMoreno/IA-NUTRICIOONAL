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
| Plantillas | Jinja2 (server-side) |
| Autenticación | Flask-Login (sesiones con cookies) |
| Contraseñas | bcrypt |

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
│   ├── __init__.py        # Fábrica create_app()
│   ├── config.py          # Configuración desde .env
│   ├── extensions.py      # db, login_manager, migrate, csrf
│   ├── models.py          # Modelos: User, Evaluacion
│   │
│   ├── main/              # Blueprint público
│   │   ├── __init__.py
│   │   └── routes.py      # / → Página principal (landing + login/register)
│   │
│   ├── auth/              # Blueprint de autenticación
│   │   ├── __init__.py
│   │   └── routes.py      # /auth/api/login, /auth/api/register, /auth/api/logout
│   │
│   ├── dashboard/         # Blueprint del usuario común
│   │   ├── __init__.py
│   │   └── routes.py      # /dashboard, /dashboard/evaluar, /dashboard/resultados/<id>
│   │
│   ├── nutritionist/      # Blueprint del nutricionista
│   │   ├── __init__.py
│   │   └── routes.py      # /nutritionist, /nutritionist/pacientes
│   │
│   ├── services/          # Lógica de negocio (no son rutas)
│   │   ├── __init__.py
│   │   ├── clinical.py    # IMC, somatotipo, agua corporal, etc.
│   │   └── nutrition.py   # TMB, calorías objetivo, macronutrientes
│   │
│   └── templates/         # Plantillas Jinja2
│       ├── main/
│       │   └── home.html          # Landing + login + register (todo en uno)
│       ├── dashboard/
│       │   ├── index.html         # Panel del usuario (historial)
│       │   ├── evaluacion.html    # Formulario de evaluación clínica
│       │   └── resultados.html    # Informe de resultados
│       └── nutritionist/
│           └── index.html         # Panel del nutricionista
│
│   ├── static/             # Archivos estáticos servidos por Flask
│   ├── css/
│   │   ├── styles.css       # Estilos de la landing
│   │   ├── evaluacion.css   # Estilos del formulario
│   │   ├── resultados.css   # Estilos del informe
│   │   └── cuenta.css       # Estilos del panel de usuario
│   ├── js/
│   │   ├── auth.js          # Login, registro, logout
│   │   ├── evaluation.js    # Validación y envío del formulario
│   │   ├── resultados.js    # Renderizado de resultados en DOM
│   │   └── utils.js         # Funciones auxiliares
│   └── img/                 # Imágenes del frontend
│       ├── login_nombre.jpg
│       ├── entrenamiento.jpg
│       └── ...
│
├── instance/              # Base de datos SQLite (se crea sola)
│   └── nutriexpert.db
│
└── server-api-docs.md     # Documentación de la API antigua (Node.js)
                            # para referencia durante la migración
```

---

## Cómo funciona

### Flujo del usuario

```
1. Landing (/) → El usuario ve la página principal
   └── Se registra o inicia sesión (todo en la misma página,
       secciones ocultas que se muestran con JS)

2. Dashboard (/dashboard) → Panel con historial de evaluaciones
   └── Botón "Nueva Evaluación" → formulario clínico

3. Evaluación (/dashboard/evaluar) → Formulario con 4 pasos:
   01. Datos personales (estatura, peso)
   02. Composición corporal (% grasa, opcional)
   03. Nivel de actividad física
   04. Objetivo principal
   └── JS valida campos y envía POST a /dashboard/api/evaluar

4. Resultados (/dashboard/resultados/<id>) → Informe completo:
   - Parámetros introducidos
   - IMC + clasificación
   - Peso ideal + rango saludable
   - Somatotipo estimado
   - Masa grasa + masa magra
   - Agua corporal (fórmula de Watson)
   - TMB (Mifflin-St Jeor)
   - Calorías objetivo
   - Distribución de macronutrientes (proteínas, carbohidratos, grasas)
```

### Flujo del nutricionista

```
1. Login como nutritionist → /nutritionist
2. Ve lista de pacientes
3. Puede ver los resultados de evaluación de cada paciente
```

---

## Blueprints (organización de rutas)

| Blueprint | Prefijo URL | ¿Qué hace? |
|---|---|---|
| `main` | `/` | Página principal (landing) |
| `auth` | `/auth` | API de login/register/logout (JSON) |
| `dashboard` | `/dashboard` | Panel del usuario común |
| `nutritionist` | `/nutritionist` | Panel del nutricionista |

Cada blueprint está en su propia carpeta con `__init__.py` y `routes.py`.
Las rutas que devuelven JSON tienen `/api/` en su path.

---

## Base de datos (SQLAlchemy)

### Modelo `User`

| Columna | Tipo | Detalle |
|---|---|---|
| id | Integer PK | |
| nombre | String(100) | |
| correo | String(100) | Único, usado para login |
| edad | Integer | |
| sexo | String(1) | M / F / O |
| contrasena_hash | String(255) | Hash de bcrypt |
| fecha_registro | DateTime | |
| role | String(20) | 'user' o 'nutritionist' |

### Modelo `Evaluacion`

| Columna | Tipo | Detalle |
|---|---|---|
| id | Integer PK | |
| usuario_id | Integer FK | Relacionado con User |
| estatura | Float | cm |
| peso | Float | kg |
| porcentaje_grasa | Float | Opcional |
| nivel_actividad | String | Ver factores de actividad |
| objetivo_principal | String | hipertrofia / mantenimiento / perdida |
| resultados | Text (JSON) | Output completo del motor clínico |
| fecha_registro | DateTime | |

---

## Servicios (lógica de negocio)

`app/services/` contiene las funciones de cálculo, separadas de las rutas:

| Archivo | Funciones |
|---|---|
| `clinical.py` | IMC, clasificación OMS, peso ideal (Devine), rango saludable, somatotipo, masa grasa/magra, agua corporal (Watson) |
| `nutrition.py` | TMB (Mifflin-St Jeor), factor de actividad, calorías objetivo por objetivo, distribución de macros |
| `__init__.py` | Función `ejecutar_analisis(datos)` que orquesta todo |

No dependen de Flask ni de la base de datos — son funciones puras
que reciben datos y devuelven resultados.

---

## Frontend

- **HTML** → Jinja2 templates en `app/templates/`
- **CSS** → Archivos separados en `static/css/`
- **JS** → Archivos separados en `static/js/`

El frontend se comunica con el backend mediante `fetch()` a las rutas
`/auth/api/*` y `/dashboard/api/*`, que devuelven JSON.

Las rutas HTML se cargan con `url_for('dashboard.index')` y los
archivos estáticos con `url_for('static', filename='css/...')`.

---

## Roles de usuario

| role | Acceso |
|---|---|
| `user` | `/dashboard/*` — evaluaciones y resultados propios |
| `nutritionist` | `/nutritionist/*` — pacientes y sus evaluaciones |

El role se asigna al crear el usuario. Por defecto es `user`.

---

## Cómo ejecutar

```bash
# 1. Activar entorno virtual
source venv/bin/activate

# 2. Inicializar base de datos (solo la primera vez)
flask init-db

# 3. Ejecutar servidor
flask run --debug
```

Abrir `http://127.0.0.1:5000/` en el navegador.
