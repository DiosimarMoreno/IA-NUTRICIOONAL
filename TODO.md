# Estado Actual del Proyecto

Todo está verificado con pruebas reales. Marca con `[x]` cuando esté hecho.

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
- [x] Registro POST `/auth/register` — bcrypt, validación, duplicados
- [x] Login POST `/auth/login` — sesión + flash messages
- [x] Logout POST `/auth/logout`
- [x] CSRF en todos los formularios
- [x] Protección `@login_required`

### D. Dashboard (usuario regular)
- [x] GET `/dashboard/` — muestra perfil + historial
- [x] GET `/dashboard/evaluar` — formulario de evaluación
- [x] POST `/dashboard/evaluar` — guarda en DB, redirige a resultados
- [x] GET `/dashboard/resultados/<id>` — muestra resultados desde DB

### E. Templates y estáticos
- [x] `home.html` — landing con login/register en tabs (JS)
- [x] `dashboard/index.html` — perfil + historial + logout
- [x] `dashboard/evaluacion.html` — formulario + validación JS
- [x] `dashboard/resultados.html` — todos los campos con Jinja2
- [x] `nutritionist/index.html` — placeholder del panel
- [x] CSS, JS e imágenes servidos desde `app/static/`

### F. Limpieza
- [x] `backend/` eliminado
- [x] `frontend/` eliminado
- [x] `server.js` eliminado
- [x] `scripts.js` eliminado
- [x] `nutriexpert.sql` eliminado
- [x] `auth/login.html` y `register.html` eliminados
- [x] `server.js:Zone.Identifier` eliminado
- [x] `services/` limpiado (engine.py, knowledge.py, routes.py, blueprint eliminados)

### G. Bugs corregidos
- [x] `dashboard/index.html` — `ev.resultados_imc` reemplazado por property `ev.imc` en el modelo
- [x] `/nutritionist/patients` — template `patients.html` creado (200 OK)
- [x] `services/` — código muerto eliminado, `__init__.py` limpio

---

## 🟡 PENDIENTE

### 1. Motor clínico real
- [ ] Crear `app/services/clinical.py` — funciones: `calcular_imc`, `clasificar_imc`, `peso_ideal_devine`, `somatotipo_estimado`, `agua_watson`
- [ ] Crear `app/services/nutrition.py` — funciones: `tmb_mifflin_stjeor`, `calorias_objetivo`, `distribuir_macros`
- [ ] Crear `app/services/schema.py` — dataclass `ResultadoEvaluacion` con todos los campos
- [ ] Conectar `dashboard.routes.evaluar_post` al motor real

### 2. Historial funcional
- [ ] Mostrar más datos (clasificación IMC, peso ideal, TMB) en la tarjeta del historial

### 3. Panel de nutricionista
- [ ] Agregar lógica de role: redirigir si `current_user.role != 'nutritionist'`
- [ ] Mostrar lista real de pacientes con evaluaciones

### 4. Varios menores
- [ ] Agregar seed de usuario nutricionista (`python seed.py` o comando flask)
- [ ] Eliminar carpeta `migrations/` si no se usa Flask-Migrate
- [ ] Verificar que `estructura.md` refleje el estado actual
