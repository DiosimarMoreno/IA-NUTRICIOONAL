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

db.connect((err) => {
    if (err) {
        console.error('Error crítico al conectar a MySQL:', err.message);
        return;
    }
    console.log('¡Conectado exitosamente a la base de datos en el puerto 3306!');
});
app.post('/api/login', (req, res) => {
    const { correo, contrasena } = req.body;

    if (!correo || !contrasena) {
        return res.status(400).json({ status: 'error', message: 'Por favor, ingresa correo y contraseña.' });
    }

    const sqlSearch = 'SELECT * FROM usuarios WHERE correo = ?';
    db.query(sqlSearch, [correo], (err, rows) => {
        if (err) {
            return res.status(500).json({ status: 'error', message: err.message });
        }

        if (rows.length === 0) {
            return res.status(401).json({ status: 'error', message: 'El correo electrónico no está registrado.' });
        }

        const usuario = rows[0];

        if (contrasena !== usuario.contrasena) {
            return res.status(401).json({ status: 'error', message: 'Contraseña incorrecta.' });
        }

        res.status(200).json({
            status: 'success',
            message: '¡Inicio de sesión exitoso! Bienvenido de nuevo.',
            usuario: {
                id: usuario.id,
                nombre: usuario.nombre,
                correo: usuario.correo
            }
        });
    });
});
app.post('/api/registrar', (req, res) => {
    const { nombre, correo, edad, sexo, contrasena } = req.body;

    if (!nombre || !correo || !edad || !sexo || !contrasena) {
        return res.status(400).json({ status: 'error', message: 'Todos los campos son obligatorios.' });
    }

    const sqlCheck = 'SELECT id FROM usuarios WHERE correo = ?';
    db.query(sqlCheck, [correo], (err, rows) => {
        if (err) {
            return res.status(500).json({ status: 'error', message: err.message });
        }

        if (rows.length > 0) {
            return res.status(400).json({ status: 'error', message: 'El correo electrónico ya está registrado.' });
        }

        const sqlInsert = 'INSERT INTO usuarios (nombre, correo, edad, sexo, contrasena) VALUES (?, ?, ?, ?, ?)';
        db.query(sqlInsert, [nombre, correo, edad, sexo, contrasena], (err, result) => {
            if (err) {
                return res.status(500).json({ status: 'error', message: err.message });
            }
            
            res.status(201).json({ status: 'success', message: '¡Cuenta creada exitosamente en Node.js!' });
        });
    });
});

const PUERTO_SERVER = 3000;
app.listen(PUERTO_SERVER, () => {
    console.log(`Servidor de Node.js corriendo en http://localhost:${PUERTO_SERVER}`);
});