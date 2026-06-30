# Estado Actual del Proyecto

---

## ✅ YA FUNCIONA (verificado)

### A. App Flask
- [x] Arranque sin errores (`python run.py`)
- [x] Config desde `.env` (`SECRET_KEY`, `DATABASE_URL`)
- [x] Blueprints registrados: `main`, `auth`, `dashboard`, `nutritionist`

### B. Base de datos (SQLite)
- [x] Modelo `User` con campos: nombre, correo, edad, sexo, contrasena_hash, role, fecha_registro
- [x] Modelo `Evaluacion` con campos: estatura, peso, porcentaje_grasa, nivel_actividad, objetivo_principal, resultados (JSON text), fecha_registro
- [x] Relación uno-a-muchos con cascade delete
- [x] Comando `flask init-db` crea las tablas

### C. Autenticación (Flask-Login)
- [x] Registro POST `/auth/register` — werkzeug.security, validación, duplicados
- [x] Login POST `/auth/login` — sesión + flash messages
- [x] Logout POST `/auth/logout`
- [x] CSRF en todos los formularios
- [x] Protección `@login_required`

### D. Dashboard (usuario regular)
- [x] GET `/dashboard/` — muestra perfil + historial
- [x] GET `/dashboard/evaluar` — formulario de evaluación
- [x] POST `/dashboard/evaluar` — guarda en DB, redirige a resultados
- [x] GET `/dashboard/resultados/<id>` — muestra resultados desde DB
- [x] GET `/dashboard/plan-accion/<id>` — plan de acción personalizado

### E. Templates y estáticos
- [x] `home.html` — landing con login/register en tabs (JS)
- [x] `dashboard/index.html` — perfil + historial + logout
- [x] `dashboard/evaluacion.html` — formulario + validación JS
- [x] `dashboard/resultados.html` — todos los campos con Jinja2
- [x] `dashboard/plan_accion.html` — plan de acción personalizado
- [x] `nutritionist/index.html` — placeholder del panel
- [x] `nutritionist/patients.html` — placeholder de pacientes
- [x] CSS, JS e imágenes servidos desde `app/static/`

### F. Limpieza
- [x] `backend/` eliminado
- [x] `frontend/` eliminado
- [x] `server.js` eliminado
- [x] `scripts.js` eliminado
- [x] `nutriexpert.sql` eliminado
- [x] `auth/login.html` y `register.html` eliminados (todo en `home.html`)
- [x] `server.js:Zone.Identifier` eliminado
- [x] `services/` reconstruido con nuevo motor (código muerto eliminado)
- [x] `server-api-docs.md` eliminado (docs del antiguo backend Node.js)

### G. Bugs corregidos
- [x] `dashboard/index.html` — `ev.resultados_imc` reemplazado por property `ev.imc` en el modelo
- [x] `/nutritionist/patients` — template `patients.html` creado (200 OK)
- [x] `services/` — código muerto eliminado, `__init__.py` limpio

### H. Motor clínico (sistema experto)
- [x] `app/services/clinical_knowledge.py` — funciones: `calcular_imc`, `clasificar_imc`, `peso_ideal_devine`, `rango_saludable`, `somatotipo_por_grasa`, `somatotipo_por_imc`, `estimar_grasa_deurenberg`, `masa_grasa_kg`, `masa_magra_kg`, `agua_watson`
- [x] `app/services/nutritional_knowledge.py` — funciones: `tmb_mifflin_stjeor`, `factor_actividad`, `calorias_objetivo`, `distribuir_macros`
- [x] `app/services/evaluation_schema.py` — dataclass `ResultadoEvaluacion` con 26 campos + `to_dict()`
- [x] `app/services/inference_engine.py` — motor forward-chaining con disparo por etapas
- [x] `app/services/knowledge_base.py` — 40 reglas clínicas en 6 módulos (validación, antropométrico, metabólico, adaptación, prescripción, riesgos)
- [x] `app/services/__init__.py` — `ejecutar_analisis(datos)` orquesta el motor completo
- [x] `dashboard.routes.evaluar_post` conectado al motor real vía `ejecutar_analisis()`

---

## 🟡 PENDIENTE

### 1. Historial funcional
- [ ] Mostrar más datos (clasificación IMC, peso ideal, TMB) en la tarjeta del historial (`dashboard/index.html`)

### 2. Panel de nutricionista
- [ ] Agregar lógica de role: redirigir si `current_user.role != 'nutritionist'`
- [ ] Mostrar lista real de pacientes con evaluaciones

### 3. Varios menores
- [ ] Agregar seed de usuario nutricionista (`python seed.py` o comando flask)
- [ ] Verificar que `estructura.md` refleje el estado actual
- [ ] Verificar que `README.md` refleje el estado actual
