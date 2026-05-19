import streamlit as st
from pacientes import agregar_paciente, listar_pacientes, obtener_paciente, modificar_paciente
from sesiones import agregar_sesion, listar_sesiones_paciente, listar_sesiones_pendientes, marcar_cobrado
from reportes import ingresos_por_mes, ingresos_por_paciente, ingresos_por_patologia
from database import crear_tablas

crear_tablas()

st.set_page_config(page_title="Consultorio", layout="wide")
st.title("🧠 Consultorio Psicológico")

menu = st.sidebar.selectbox("Menú", [
    "Resumen",
    "Pacientes",
    "Nueva Sesión",
    "Sesiones Pendientes",
    "Reportes"
])

if menu == "Resumen":
    st.subheader("Resumen general")
    pacientes = listar_pacientes()
    pendientes = listar_sesiones_pendientes()
    col1, col2 = st.columns(2)
    col1.metric("Pacientes activos", len(pacientes))
    col2.metric("Sesiones sin cobrar", len(pendientes))

elif menu == "Pacientes":
    tab1, tab2 = st.tabs(["Listado", "Nuevo Paciente"])

    with tab1:
        st.subheader("Pacientes activos")
        pacientes = listar_pacientes()
        if pacientes:
            for p in pacientes:
                st.write(f"**{p[2]}, {p[1]}** — {p[3]} | {p[4]} | {p[5]} | {p[6]} {p[7]} | {p[8]}")
        else:
            st.info("No hay pacientes cargados.")

    with tab2:
        st.subheader("Nuevo paciente")
        with st.form("form_paciente"):
            col1, col2 = st.columns(2)
            nombre = col1.text_input("Nombre")
            apellido = col2.text_input("Apellido")
            fecha_nacimiento = col1.date_input("Fecha de nacimiento")
            telefono = col1.text_input("Teléfono")
            email = col2.text_input("Email")
            fecha_primera_consulta = col2.date_input("Primera consulta")
            patologia = st.text_input("Patología / Motivo de consulta")
            col3, col4 = st.columns(2)
            modalidad = col3.selectbox("Modalidad", ["presencial", "online"])
            tipo = col4.selectbox("Tipo", ["particular", "obra social"])
            obra_social = st.text_input("Obra social (si aplica)")
            col5, col6 = st.columns(2)
            moneda = col5.selectbox("Moneda", ["ARS", "USD", "EUR"])
            precio_sesion = col6.number_input("Precio por sesión", min_value=0.0)
            pais_residencia = st.text_input("País de residencia")

            if st.form_submit_button("Guardar paciente"):
                agregar_paciente(nombre, apellido, str(fecha_nacimiento), telefono,
                                 email, str(fecha_primera_consulta), patologia,
                                 modalidad, tipo, obra_social, moneda,
                                 precio_sesion, pais_residencia)
                st.success(f"Paciente {nombre} {apellido} guardado correctamente.")

elif menu == "Nueva Sesión":
    st.subheader("Registrar sesión")
    pacientes = listar_pacientes()
    if not pacientes:
        st.warning("Primero cargá un paciente.")
    else:
        opciones = {f"{p[2]}, {p[1]}": p[0] for p in pacientes}
        seleccion = st.selectbox("Paciente", list(opciones.keys()))
        id_paciente = opciones[seleccion]

        with st.form("form_sesion"):
            col1, col2 = st.columns(2)
            fecha = col1.date_input("Fecha")
            numero_sesion = col2.number_input("Número de sesión", min_value=1, step=1)
            modalidad = col1.selectbox("Modalidad", ["presencial", "online"])
            moneda = col2.selectbox("Moneda", ["ARS", "USD", "EUR"])
            monto_paciente = col1.number_input("Monto paciente", min_value=0.0)
            monto_obra_social = col2.number_input("Monto obra social", min_value=0.0)
            cobrado = st.selectbox("¿Cobrado?", ["no", "si"])
            forma_cobro = st.selectbox("Forma de cobro", ["efectivo", "transferencia", "obra social"])

            if st.form_submit_button("Registrar sesión"):
                agregar_sesion(id_paciente, str(fecha), numero_sesion, modalidad,
                               monto_paciente, monto_obra_social, moneda, cobrado, forma_cobro)
                st.success("Sesión registrada correctamente.")

elif menu == "Sesiones Pendientes":
    st.subheader("Sesiones sin cobrar")
    pendientes = listar_sesiones_pendientes()
    if pendientes:
        for s in pendientes:
            col1, col2 = st.columns([4, 1])
            col1.write(f"**{s[2]}, {s[1]}** — {s[3]} | {s[6]} {s[4]}")
            if col2.button("Marcar cobrado", key=s[0]):
                marcar_cobrado(s[0], "efectivo")
                st.rerun()
    else:
        st.success("No hay sesiones pendientes de cobro.")

elif menu == "Reportes":
    st.subheader("Reportes")
    anio = st.number_input("Año", min_value=2020, max_value=2030, value=2026)

    st.markdown("### Ingresos por mes")
    datos = ingresos_por_mes(anio)
    if datos:
        for d in datos:
            st.write(f"Mes {d[0]} | {d[1]} {d[2]:,.2f}")
    else:
        st.info("Sin datos para ese año.")

    st.markdown("### Ingresos por patología")
    datos = ingresos_por_patologia(anio)
    if datos:
        for d in datos:
            st.write(f"{d[0]} | {d[3]} sesiones | {d[1]} {d[3]:,.2f}")
    else:
        st.info("Sin datos.")
