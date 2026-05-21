from database import get_connection

def agregar_paciente(nombre, apellido, fecha_nacimiento, telefono, email,
                     fecha_primera_consulta, patologia, modalidad, tipo,
                     obra_social, nro_afiliado, moneda, precio_sesion, pais_residencia):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO paciente (nombre, apellido, fecha_nacimiento, telefono, email,
                              fecha_primera_consulta, patologia, modalidad, tipo,
                              obra_social, nro_afiliado, moneda, precio_sesion, pais_residencia)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (nombre, apellido, fecha_nacimiento, telefono, email,
          fecha_primera_consulta, patologia, modalidad, tipo,
          obra_social, nro_afiliado, moneda, precio_sesion, pais_residencia))

    conn.commit()
    conn.close()

def listar_pacientes():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_paciente, nombre, apellido, patologia,
               modalidad, tipo, moneda, precio_sesion, pais_residencia
        FROM paciente
        WHERE estado = 'activo'
        ORDER BY apellido, nombre
    """)

    pacientes = cursor.fetchall()
    conn.close()
    return pacientes

def obtener_paciente(id_paciente):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM paciente WHERE id_paciente = ?", (id_paciente,))
    paciente = cursor.fetchone()
    conn.close()
    return paciente

def modificar_paciente(id_paciente, nombre, apellido, fecha_nacimiento, telefono,
                       email, patologia, modalidad, tipo, obra_social, nro_afiliado,
                       moneda, precio_sesion, pais_residencia, estado):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE paciente SET nombre=?, apellido=?, fecha_nacimiento=?, telefono=?,
               email=?, patologia=?, modalidad=?, tipo=?, obra_social=?,
               nro_afiliado=?, moneda=?, precio_sesion=?, pais_residencia=?, estado=?
        WHERE id_paciente=?
    """, (nombre, apellido, fecha_nacimiento, telefono, email, patologia,
          modalidad, tipo, obra_social, nro_afiliado, moneda, precio_sesion,
          pais_residencia, estado, id_paciente))

    conn.commit()
    conn.close()
