import streamlit as st
from pacientes import agregar_paciente, listar_pacientes, obtener_paciente, modificar_paciente
from sesiones import agregar_sesion, listar_sesiones_paciente, listar_sesiones_pendientes, marcar_cobrado
from reportes import ingresos_por_mes, ingresos_por_paciente
from database import crear_tablas
from datetime import date

crear_tablas()

st.set_page_config(page_title="Consultorio", layout="wide")
st.title("Consultorio Psicológico")

menu = st.sidebar.selectbox("Menú", [
    "Resumen",
    "Pacientes",
    "Nueva Sesión",
    "Sesiones Pendientes",
    "Reportes"
])

# ─── RESUMEN ───────────────────────────────────────────────
if menu == "Resumen":
    st.subheader("Resumen general")
    pacientes = listar_pacientes()
    pendientes = listar_sesiones_pendientes()
    col1, col2 = st.columns(2)
    col1.metric("Pacientes activos", len(pacientes))
    col2.metric("Sesiones sin cobrar", len(pendientes))

    if pendientes:
        st.markdown("### Sesiones pendientes de cobro")
        for s in pendientes:
            st.write(f"**{s[2]}, {s[1]}** — {s[3]} | {s[6]} {s[4]}")

# ─── PACIENTES ─────────────────────────────────────────────
elif menu == "Pacientes":
    tab1, tab2 = st.tabs(["Listado y edición", "Nuevo Paciente"])

    with tab1:
        st.subheader("Pacientes activos")
        pacientes = listar_pacientes()
        if not pacientes:
            st.info("No hay pacientes cargados.")
        else:
            opciones = {f"{p[2]}, {p[1]}": p[0] for p in pacientes}
            seleccion = st.selectbox("Seleccionar paciente", list(opciones.keys()))
            id_sel = opciones[seleccion]
            p = obtener_paciente(id_sel)

            with st.form("form_editar"):
                st.markdown("#### Datos del paciente")
                nombre = st.text_input("Nombre", value=p[1])
                apellido = st.text_input("Apellido", value=p[2])
                
                try:
                    fn = date.fromisoformat(p[3]) if p[3] else date(1980, 1, 1)
                except:
                    fn = date(1980, 1, 1)
                fecha_nacimiento = st.date_input(
                    "Fecha de nacimiento (aaaa/mm/dd)",
                    value=fn,
                    min_value=date(1900, 1, 1),
                    max_value=date(2030, 12, 31)
                )
                telefono = st.text_input("Teléfono", value=p[4] or "")
                email = st.text_input("Email", value=p[5] or "")
                
                try:
                    fpc = date.fromisoformat(p[6]) if p[6] else date.today()
                except:
                    fpc = date.today()
                fecha_primera_consulta = st.date_input(
                    "Primera consulta",
                    value=fpc,
                   min_value=date(2000, 1, 1),
                   max_value=date(2030, 12, 31)
                )
                patologia = st.text_input("Patología / Motivo", value=p[7] or "")
                modalidad = st.selectbox("Modalidad", ["presencial", "online"],
                    index=0 if p[8] == "presencial" else 1)
                tipo = st.selectbox("Tipo", ["particular", "obra social"],
                    index=0 if p[9] == "particular" else 1)
                obra_social = st.text_input("Obra social", value=p[10] or "")
                moneda = st.selectbox("Moneda", ["ARS", "USD", "EUR"],
                    index=["ARS","USD","EUR"].index(p[11]) if p[11] in ["ARS","USD","EUR"] else 0)
                precio_sesion = st.number_input("Precio por sesión", 
                    min_value=0.0, value=float(p[12] or 0))
                pais_residencia = st.text_input("País de residencia", value=p[13] or "")
                estado = st.selectbox("Estado", ["activo", "inactivo"],
                    index=0 if p[14] == "activo" else 1)

                if st.form_submit_button("Guardar cambios"):
                    modificar_paciente(id_sel, nombre, apellido, str(fecha_nacimiento),
                                      telefono, email, patologia, modalidad, tipo,
                                      obra_social, moneda, precio_sesion,
                                      pais_residencia, estado)
                   
                    st.success("Paciente actualizado correctamente.")
                    st.rerun()

            st.markdown("#### Sesiones del paciente")
            sesiones = listar_sesiones_paciente(id_sel)
            if sesiones:
                for s in sesiones:
                    cobrado_txt = "✅" if s[7] == "si" else "❌"
                    st.write(f"Sesión {s[2]} | {s[1]} | {s[3]} | {s[6]} {s[4]} pac. / {s[5]} OS | {cobrado_txt} {s[8]}")
            else:
                st.info("Sin sesiones registradas.")

    with tab2:
        st.subheader("Nuevo paciente")
        with st.form("form_paciente"):
            nombre = st.text_input("Nombre")
            apellido = st.text_input("Apellido")
            fecha_nacimiento = st.date_input(
                    "Fecha de nacimiento (aaaa/mm/dd)",
                    value=fn,
                    min_value=date(1900, 1, 1),
                    max_value=date(2030, 12, 31)
            )
            telefono = st.text_input("Teléfono")
            email = st.text_input("Email")

            fecha_primera_consulta = st.date_input(
                "Primera consulta",
                 value=fpc,
                 min_value=date(2000, 1, 1),
                 max_value=date(2030, 12, 31)
            )
            patologia = st.text_input("Patología / Motivo de consulta")
            modalidad = st.selectbox("Modalidad", ["presencial", "online"])
            tipo = st.selectbox("Tipo", ["particular", "obra social"])
            obra_social = st.text_input("Obra social (si aplica)")
            moneda = st.selectbox("Moneda", ["ARS", "USD", "EUR"])
            precio_sesion = st.number_input("Precio por sesión", min_value=0.0)
            pais_residencia = st.text_input("País de residencia")

      if st.form_submit_button("Guardar paciente"):
                if nombre and apellido:
                    pacientes_existentes = listar_pacientes()
                    duplicado = any(
                        p[1].lower() == nombre.lower() and p[2].lower() == apellido.lower()
                        for p in pacientes_existentes
                    )
                    if duplicado:
                        st.error(f"Ya existe un paciente con el nombre {nombre} {apellido}.")
                    else:
                        agregar_paciente(nombre, apellido, str(fecha_nacimiento), telefono,
                                         email, str(fecha_primera_consulta), patologia,
                                         modalidad, tipo, obra_social, moneda,
                                         precio_sesion, pais_residencia)
                        st.success(f"Paciente {nombre} {apellido} guardado correctamente.")
                else:
                    st.error("Nombre y apellido son obligatorios.")

# ─── NUEVA SESIÓN ──────────────────────────────────────────
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
            fecha = st.date_input(
                "Fecha de sesión",
                value=date.today(),
                format="DD/MM/YYYY"
            )
            numero_sesion = st.number_input("Número de sesión", min_value=1, step=1)
            modalidad = st.selectbox("Modalidad", ["presencial", "online"])
            moneda = st.selectbox("Moneda", ["ARS", "USD", "EUR"])
            monto_paciente = st.number_input("Monto paciente", min_value=0.0)
            monto_obra_social = st.number_input("Monto obra social", min_value=0.0)
            cobrado = st.selectbox("¿Cobrado?", ["no", "si"])
            forma_cobro = st.selectbox("Forma de cobro", ["efectivo", "transferencia", "obra social"])

            if st.form_submit_button("Registrar sesión"):
                agregar_sesion(id_paciente, str(fecha), numero_sesion, modalidad,
                               monto_paciente, monto_obra_social, moneda, cobrado, forma_cobro)
                st.success("Sesión registrada correctamente.")

# ─── SESIONES PENDIENTES ───────────────────────────────────
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

# ─── REPORTES ──────────────────────────────────────────────
elif menu == "Reportes":
    st.subheader("Reportes de ingresos")
    anio = st.number_input("Año", min_value=2020, max_value=2030, value=2026, step=1)
    meses = {
        "01": "Enero", "02": "Febrero", "03": "Marzo", "04": "Abril",
        "05": "Mayo", "06": "Junio", "07": "Julio", "08": "Agosto",
        "09": "Septiembre", "10": "Octubre", "11": "Noviembre", "12": "Diciembre"
    }

    datos_mes = ingresos_por_mes(anio)
    if not datos_mes:
        st.info("Sin datos para ese año.")
    else:
        for mes, moneda, total_mes in datos_mes:
            st.markdown(f"### {meses.get(mes, mes)} — {moneda} {total_mes:,.2f}")
            datos_pac = ingresos_por_paciente(anio, mes)
            
            particular_total = 0
            os_dict = {}
            
            for d in datos_pac:
                nombre_pac = f"{d[1]}, {d[0]}"
                os = d[2] if d[2] else "Particular"
                sesiones = d[4]
                total = d[5]
                
                if not d[2]:
                    particular_total += total
                    st.write(f"&nbsp;&nbsp;&nbsp;{nombre_pac} | {sesiones} ses. | {moneda} {total:,.2f}")
                else:
                    if os not in os_dict:
                        os_dict[os] = {"total": 0, "pacientes": []}
                    os_dict[os]["total"] += total
                    os_dict[os]["pacientes"].append((nombre_pac, sesiones, total))
            
            if os_dict:
                for os_nombre, os_data in os_dict.items():
                    st.markdown(f"**Obra Social: {os_nombre}** — subtotal {moneda} {os_data['total']:,.2f}")
                    for pac, ses, tot in os_data["pacientes"]:
                        st.write(f"&nbsp;&nbsp;&nbsp;{pac} | {ses} ses. | {moneda} {tot:,.2f}")
            
            st.markdown("---")
