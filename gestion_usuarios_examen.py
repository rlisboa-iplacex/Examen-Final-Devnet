#!/usr/bin/env python3

import sqlite3          # Base de datos para usuarios
import hashlib          # Hash de contraseñas
from flask import Flask, request

app = Flask(__name__)

db_name = 'usuarios_examen.db'

# -----------------------------
# Funciones de base de datos
# -----------------------------
def crear_bd():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def registrar_usuario(usuario, password):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    hash_pw = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("INSERT INTO usuarios (usuario, password_hash) VALUES (?, ?)", (usuario, hash_pw))
    conn.commit()
    conn.close()

def validar_usuario(usuario, password):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM usuarios WHERE usuario = ?", (usuario,))
    row = cursor.fetchone()
    conn.close()

    if row:
        hash_ingresado = hashlib.sha256(password.encode()).hexdigest()
        return hash_ingresado == row[0]
    else:
        return False

# -----------------------------
# Rutas Flask
# -----------------------------

@app.route("/")
def index():
    return "Servicio de gestión de usuarios del examen Devnet en ejecución."

# Registro de usuarios vía curl
@app.route("/signup/v1", methods=["POST"])
def signup():
    usuario = request.form.get("username", "")
    password = request.form.get("password", "")

    if not usuario or not password:
        return "Faltan parametros", 400

    registrar_usuario(usuario, password)
    return "Registro exitoso", 200

# Validación de usuarios vía curl
@app.route("/login/v1", methods=["POST"])
def login():
    usuario = request.form.get("username", "")
    password = request.form.get("password", "")

    if not usuario or not password:
        return "Faltan parametros", 400

    if validar_usuario(usuario, password):
        return "Validacion exitosa", 200
    else:
        return "Credenciales invalidas", 401

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    crear_bd()
    # Servidor HTTPS con cert.pem y key.pem
    app.run(host="0.0.0.0", port=5800, ssl_context=("cert.pem", "key.pem"))

