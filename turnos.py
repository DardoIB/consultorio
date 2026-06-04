from database import get_connection
from datetime import datetime

def agregar_turno(nombre, email, telefono, modalidad, fecha, hora, mensaje):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO turno_solicitado 
        (nombre, email, telefono, modalidad, fecha, hora, mensaje, fecha_solicitud)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (nombre, email, telefono, modalidad, fecha, hora, mensaje,
          datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()

def listar_turnos_pendientes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_turno, nombre, email, telefono, modalidad, 
               fecha, hora, mensaje, fecha_solicitud
        FROM turno_solicitado
        WHERE estado = 'pendiente'
        ORDER BY fecha, hora
    """)
    turnos = cursor.fetchall()
    conn.close()
    return turnos

def confirmar_turno(id_turno):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE turno_solicitado SET estado = 'confirmado'
        WHERE id_turno = ?
    """, (id_turno,))
    conn.commit()
    conn.close()

def cancelar_turno(id_turno):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE turno_solicitado SET estado = 'cancelado'
        WHERE id_turno = ?
    """, (id_turno,))
    conn.commit()
    conn.close()

def horarios_ocupados(fecha):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT hora FROM turno_solicitado
        WHERE fecha = ? AND estado != 'cancelado'
    """, (fecha,))
    ocupados = [r[0] for r in cursor.fetchall()]
    conn.close()
    return ocupados
