# API de Node.js (server.js) — Documentación para migrar a Flask

Este documento describe los endpoints que implementaba el servidor Express
para replicar su funcionalidad en Flask.

---

## Endpoints

### POST /api/registrar

Registro de nuevo usuario.

**Request:**
```json
{
  "nombre": "Juan García",
  "correo": "juan@email.com",
  "edad": 25,
  "sexo": "M",
  "contrasena": "123456"
}
```

**Respuesta exitosa (201):**
```json
{
  "status": "success",
  "message": "¡Cuenta creada exitosamente en Node.js!"
}
```

**Respuesta error (400):**
```json
{
  "status": "error",
  "message": "El correo electrónico ya está registrado."
}
```

**Validaciones:**
- Todos los campos son obligatorios
- El correo debe ser único

---

### POST /api/login

Inicio de sesión.

**Request:**
```json
{
  "correo": "juan@email.com",
  "contrasena": "123456"
}
```

**Respuesta exitosa (200):**
```json
{
  "status": "success",
  "message": "¡Inicio de sesión exitoso! Bienvenido de nuevo.",
  "usuario": {
    "id": 1,
    "nombre": "Juan García",
    "correo": "juan@email.com"
  }
}
```

**Respuesta error (401):**
```json
{
  "status": "error",
  "message": "Contraseña incorrecta."
}
```

---

## CS (server.js)

```javascript
const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

const db = mysql.createConnection({
    host: 'localhost',
    port: 3306,
    user: 'root',
    password: '',
    database: 'nutriexpert'
});

app.post('/api/login', (req, res) => { ... });
app.post('/api/registrar', (req, res) => { ... });

app.listen(3000);
```

## Base de datos MySQL

**Base de datos:** `nutriexpert`
**Tabla:** `usuarios`

Estructura de la tabla (del dump `nutriexpert.sql`):
| Columna | Tipo |
|---|---|
| id | INT AUTO_INCREMENT PK |
| nombre | VARCHAR(100) NOT NULL |
| correo | VARCHAR(100) UNIQUE NOT NULL |
| edad | INT NOT NULL |
| sexo | VARCHAR(1) NOT NULL |
| contrasena | VARCHAR(255) NOT NULL |
| fecha_registro | DATETIME DEFAULT CURRENT_TIMESTAMP |

---

## Diferencias con la implementación Flask (TODO)

| Aspecto | Node.js (actual) | Flask (futuro) |
|---|---|---|
| Contraseñas | Texto plano ❌ | Hash con bcrypt ✅ |
| Rutas | `POST /api/login` | `POST /auth/api/login` |
| Sesión | JWT (no implementado, solo devuelve usuario) | Flask-Login con cookies |
| DB | MySQL | SQLite |
| CORS | Necesario (frontend en otro puerto) | No necesario (Flask sirve frontend y API) |
