from supabase_client import supabase


def agregar_paciente(nombre, apellido, fecha_nacimiento, telefono, email,
                     fecha_primera_consulta, patologia, modalidad, tipo,
                     obra_social, nro_afiliado, moneda, precio_sesion,
                     pais_residencia):

    resultado = supabase.table("paciente").insert({
        "nombre": nombre,
        "apellido": apellido,
        "fecha_nacimiento": fecha_nacimiento,
        "telefono": telefono,
        "email": email,
        "fecha_primera_consulta": fecha_primera_consulta,
        "patologia": patologia,
        "modalidad": modalidad,
        "tipo": tipo,
        "obra_social": obra_social,
        "nro_afiliado": nro_afiliado,
        "moneda": moneda,
        "precio_sesion": precio_sesion,
        "pais_residencia": pais_residencia,
        "estado": "activo"
    }).execute()

    return resultado


def listar_pacientes():

    resultado = (
        supabase
        .table("paciente")
        .select("*")
        .eq("estado", "activo")
        .order("apellido")
        .execute()
    )

    return resultado.data


def obtener_paciente(id_paciente):

    resultado = (
        supabase
        .table("paciente")
        .select("*")
        .eq("id_paciente", id_paciente)
        .execute()
    )

    if resultado.data:
        return resultado.data[0]

    return None


def modificar_paciente(id_paciente, nombre, apellido, fecha_nacimiento,
                       telefono, email, patologia, modalidad, tipo,
                       obra_social, nro_afiliado, moneda,
                       precio_sesion, pais_residencia, estado):

    supabase.table("paciente").update({
        "nombre": nombre,
        "apellido": apellido,
        "fecha_nacimiento": fecha_nacimiento,
        "telefono": telefono,
        "email": email,
        "patologia": patologia,
        "modalidad": modalidad,
        "tipo": tipo,
        "obra_social": obra_social,
        "nro_afiliado": nro_afiliado,
        "moneda": moneda,
        "precio_sesion": precio_sesion,
        "pais_residencia": pais_residencia,
        "estado": estado
    }).eq("id_paciente", id_paciente).execute()
