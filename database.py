import sqlite3

DB_PATH = "consultorio.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def crear_tablas():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS paciente (
            id_paciente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            fecha_nacimiento TEXT,
            telefono TEXT,
            email TEXT,
            fecha_primera_consulta TEXT,
            patologia TEXT,
            modalidad TEXT,
            tipo TEXT,
            obra_social TEXT,
            moneda TEXT,
            precio_sesion REAL,
            pais_residencia TEXT,
            nro_afiliado TEXT,
            estado TEXT DEFAULT 'activo'
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sesion (
            id_sesion INTEGER PRIMARY KEY AUTOINCREMENT,
            id_paciente INTEGER NOT NULL,
            fecha TEXT,
            numero_sesion INTEGER,
            modalidad TEXT,
            monto_paciente REAL,
            monto_obra_social REAL,
            moneda TEXT,
            cobrado TEXT DEFAULT 'no',
            forma_cobro TEXT,
            FOREIGN KEY (id_paciente) REFERENCES paciente(id_paciente)
        )
    """)

    conn.commit()
    conn.close()
