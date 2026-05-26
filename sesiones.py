from database import get_connection

def agregar_sesion(id_paciente, fecha, numero_sesion, modalidad,
                   monto_paciente, monto_obra_social, moneda, cobrado, forma_cobro):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sesion (id_paciente, fecha, numero_sesion, modalidad,
                            monto_paciente, monto_obra_social, moneda, cobrado, forma_cobro)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (id_paciente, fecha, numero_sesion, modalidad,
          monto_paciente, monto_obra_social, moneda, cobrado, forma_cobro))

    conn.commit()
    conn.close()

def listar_sesiones_paciente(id_paciente):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT s.id_sesion, s.fecha, s.numero_sesion, s.modalidad,
               s.monto_paciente, s.monto_obra_social, s.moneda, s.cobrado, s.forma_cobro
        FROM sesion s
        WHERE s.id_paciente = ?
        ORDER BY s.fecha DESC
    """, (id_paciente,))

    sesiones = cursor.fetchall()
    conn.close()
    return sesiones

def listar_sesiones_pendientes():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT s.id_sesion, p.nombre, p.apellido, s.fecha,
               s.monto_paciente, s.monto_obra_social, s.moneda
        FROM sesion s
        JOIN paciente p ON s.id_paciente = p.id_paciente
        WHERE s.cobrado = 'no'
        ORDER BY s.fecha
    """)

    pendientes = cursor.fetchall()
    conn.close()
    return pendientes

def marcar_cobrado(id_sesion, forma_cobro):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE sesion SET cobrado = 'si', forma_cobro = ?
        WHERE id_sesion = ?
    """, (forma_cobro, id_sesion))

    conn.commit()
    conn.close()

def ultimo_numero_sesion(id_paciente):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT MAX(numero_sesion) FROM sesion WHERE id_paciente = ?
    """, (id_paciente,))
    resultado = cursor.fetchone()[0]
    conn.close()
    return (resultado or 0) + 1

def ultima_sesion_fecha(id_paciente):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT MAX(fecha) FROM sesion WHERE id_paciente = ?
    """, (id_paciente,))
    resultado = cursor.fetchone()[0]
    conn.close()
    return resultado

def sesion_duplicada(id_paciente, fecha):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM sesion 
        WHERE id_paciente = ? AND fecha = ?
    """, (id_paciente, fecha))
    resultado = cursor.fetchone()[0]
    conn.close()
    return resultado > 0
