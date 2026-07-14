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
- [x] `app/services/evaluation_schema.py` — dataclass `ResultadoEvaluacion` con 30 campos + `to_dict()`
- [x] `app/services/inference_engine.py` — motor forward-chaining con disparo por etapas
- [x] `app/services/knowledge_base.py` — 40 reglas clínicas en 6 módulos (validación, antropométrico, metabólico, adaptación, prescripción, riesgos)
- [x] `app/services/__init__.py` — `ejecutar_analisis(datos)` orquesta el motor completo
- [x] `dashboard.routes.evaluar_post` conectado al motor real vía `ejecutar_analisis()`

### I. Protección por roles
- [x] Decorador `@role_required(role)` en `app/decorators.py`
- [x] Dashboard protegido con `@role_required('user')` en todas sus rutas
- [x] Panel nutricionista protegido con `@role_required('nutritionist')` en todas sus rutas
- [x] Redirects de `auth/login` y `auth/register` según el rol del usuario autenticado

---

## 🟡 PENDIENTE

### 1. Frontend de usuario — Historial (`dashboard/index.html`)
- [ ] Mostrar en cada tarjeta: clasificación IMC (con badge de color según OMS), peso ideal (Devine), TMB (kcal), calorías objetivo, somatotipo
- [ ] Indicador visual de riesgo metabólico (color: verde/amarillo/rojo según `riesgo_metabolico`)
- [ ] Enlaces directos a "Ver resultados" y "Ver plan de acción" por evaluación
- [ ] Badge con el objetivo de la evaluación (hipertrofia/mantenimiento/pérdida)

### 2. Frontend de usuario — Reporte de resultados (`resultados.html`)
- [ ] Mostrar `riesgo_metabolico` con badge de alerta (bajo/moderado/alto)
- [ ] Mostrar `riesgo_nutricional` con indicador visual
- [ ] Mostrar lista de `alertas` con íconos de advertencia
- [ ] Mostrar `recomendaciones` numeradas como lista de acción
- [ ] Mostrar `nota_clinica` como bloque destacado al final del reporte
- [ ] Mostrar `explicaciones` como sección colapsable (accordion)
- [ ] Mostrar `factor_actividad` junto a la TMB y el gasto energético total

### 3. Frontend de usuario — Plan de acción (`plan_accion.html`)
- [ ] Reemplazar contenido hardcodeado (comidas, ejercicios, rutinas) con datos reales del motor clínico
- [ ] Personalizar el plan según `objetivo_etiqueta` (hipertrofia / mantenimiento / pérdida)
- [ ] Incorporar `recomendaciones` y `nota_clinica` dentro del plan
- [ ] Mostrar distribución de macros visual (barras de progreso o gráfico)

### 4. Frontend de usuario — Mejoras UX generales
- [ ] Estado vacío mejorado cuando no hay evaluaciones (icono + mensaje + CTA)
- [ ] Animaciones de carga/transición entre vistas del dashboard
- [ ] Diseño responsive para tablets y móviles

### 5. Frontend de nutricionista — Panel principal (`nutritionist/index.html`)
- [ ] Navbar con logo, nombre del nutricionista, botón de cerrar sesión
- [ ] Tarjetas de resumen: total pacientes, total evaluaciones, pacientes con riesgo alto
- [ ] Lista de pacientes con búsqueda por nombre/correo
- [ ] Cada paciente en lista muestra: nombre, correo, última evaluación (fecha + IMC)
- [ ] Enlace para ver detalle de cada paciente

### 6. Frontend de nutricionista — Vista de paciente individual
- [ ] Crear ruta `GET /nutritionist/patient/<int:id>` con template
- [ ] Mostrar datos del paciente: nombre, edad, sexo, correo, fecha de registro
- [ ] Historial completo de evaluaciones del paciente
- [ ] Cada evaluación muestra: fecha, IMC + clasificación OMS, peso, TMB, calorías objetivo
- [ ] Enlace a reporte completo de cada evaluación

### 7. Frontend de nutricionista — Lista de pacientes (`nutritionist/patients.html`)
- [ ] Tabla de pacientes con columnas: nombre, correo, cantidad de evaluaciones, última actividad
- [ ] Paginación si hay más de 20 pacientes
- [ ] Filtros por rango de fechas y estado de riesgo

### 8. Backend — Rutas de nutricionista
- [ ] Implementar queries: obtener todos los usuarios con evaluaciones, contar evaluaciones por paciente, obtener última evaluación de cada paciente
- [ ] Ruta `GET /nutritionist/patient/<int:id>` con datos completos del paciente

### 9. Varios menores
- [ ] Verificar que `estructura.md` refleje el estado actual
- [ ] Verificar que `README.md` refleje el estado actual
