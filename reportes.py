from database import get_connection

def ingresos_por_mes(anio):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            strftime('%m', s.fecha) as mes,
            s.moneda,
            SUM(s.monto_paciente + COALESCE(s.monto_obra_social, 0)) as total
        FROM sesion s
        WHERE strftime('%Y', s.fecha) = ?
        AND s.cobrado = 'si'
        GROUP BY mes, s.moneda
        ORDER BY mes
    """, (str(anio),))

    resultado = cursor.fetchall()
    conn.close()
    return resultado

def ingresos_por_paciente(anio, mes=None):
    conn = get_connection()
    cursor = conn.cursor()

    if mes:
        cursor.execute("""
            SELECT 
                p.nombre, p.apellido, p.patologia,
                s.moneda,
                COUNT(s.id_sesion) as cant_sesiones,
                SUM(s.monto_paciente + COALESCE(s.monto_obra_social, 0)) as total
            FROM sesion s
            JOIN paciente p ON s.id_paciente = p.id_paciente
            WHERE strftime('%Y', s.fecha) = ?
            AND strftime('%m', s.fecha) = ?
            AND s.cobrado = 'si'
            GROUP BY p.id_paciente, s.moneda
            ORDER BY total DESC
        """, (str(anio), str(mes).zfill(2)))
    else:
        cursor.execute("""
            SELECT 
                p.nombre, p.apellido, p.patologia,
                s.moneda,
                COUNT(s.id_sesion) as cant_sesiones,
                SUM(s.monto_paciente + COALESCE(s.monto_obra_social, 0)) as total
            FROM sesion s
            JOIN paciente p ON s.id_paciente = p.id_paciente
            WHERE strftime('%Y', s.fecha) = ?
            AND s.cobrado = 'si'
            GROUP BY p.id_paciente, s.moneda
            ORDER BY total DESC
        """, (str(anio),))

    resultado = cursor.fetchall()
    conn.close()
    return resultado

def ingresos_por_patologia(anio):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            p.patologia,
            s.moneda,
            COUNT(s.id_sesion) as cant_sesiones,
            SUM(s.monto_paciente + COALESCE(s.monto_obra_social, 0)) as total
        FROM sesion s
        JOIN paciente p ON s.id_paciente = p.id_paciente
        WHERE strftime('%Y', s.fecha) = ?
        AND s.cobrado = 'si'
        GROUP BY p.patologia, s.moneda
        ORDER BY total DESC
    """, (str(anio),))

    resultado = cursor.fetchall()
    conn.close()
    return resultado
