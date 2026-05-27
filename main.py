import streamlit as st
from pacientes import agregar_paciente, listar_pacientes, obtener_paciente, modificar_paciente
from sesiones import agregar_sesion, listar_sesiones_paciente, listar_sesiones_pendientes, marcar_cobrado
from reportes import ingresos_por_mes, ingresos_por_paciente
from database import crear_tablas
from datetime import date

crear_tablas()

st.set_page_config(page_title="Consultorio", layout="wide")

st.markdown("""
    <style>
        .block-container { 
            padding-top: 0.5rem; 
            padding-bottom: 0rem;
        }
        h1 { font-size: 1.4rem !important; margin-bottom: 0.3rem !important; }
        h2 { font-size: 1.1rem !important; margin-bottom: 0.2rem !important; }
        h3 { font-size: 1rem !important; margin-bottom: 0.2rem !important; }
        label { 
            font-size: 0.8rem !important; 
            color: #555 !important;
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 0.85rem;
            padding: 0.3rem 0.8rem;
        }
        .stTabs [aria-selected="true"] {
            font-weight: bold !important;
        }
    </style>
""", unsafe_allow_html=True)
st.title("Consultorio Psicológico")

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
    if pendientes:
        st.markdown("### Sesiones pendientes de cobro")
        for s in pendientes:
            st.write(f"**{s[2]}, {s[1]}** — {s[3]} | {s[6]} {s[4]}")

elif menu == "Pacientes":
    tab1, tab2, tab3 = st.tabs(["Listado y edición", "Nuevo Paciente", "Historial sesiones"])

    with tab1:
        st.subheader("Pacientes activos")
        pacientes = listar_pacientes()
        if not pacientes:
            st.info("No hay pacientes cargados.")
        else:
            opciones = {f"{p[2]}, {p[1]}": p[0] for p in pacientes}
            seleccion = st.selectbox("Seleccionar paciente", list(opciones.keys()), key="sel_paciente")
            id_sel = opciones[seleccion]
            p = obtener_paciente(id_sel)

            try:
                fn = date.fromisoformat(p[3]) if p[3] else date(1980, 1, 1)
            except:
                fn = date(1980, 1, 1)
            try:
                fpc = date.fromisoformat(p[6]) if p[6] else date.today()
            except:
                fpc = date.today()

            st.markdown("#### Datos del paciente")

            col1, col2 = st.columns(2)
            with col1:
                nombre = st.text_input("Nombre *", value=p[1], key=f"e_nombre_{id_sel}")
            with col2:
                apellido = st.text_input("Apellido *", value=p[2], key=f"e_apellido_{id_sel}")

            col1, col2, col3 = st.columns(3)
            with col1:
                fecha_nacimiento = st.date_input("Fecha de nacimiento *", value=fn,
                    min_value=date(1900, 1, 1), max_value=date.today(), key=f"e_fn_{id_sel}")
            with col2:
                telefono = st.text_input("Teléfono *", value=p[4] or "", key=f"e_tel_{id_sel}")
            with col3:
                email = st.text_input("Email *", value=p[5] or "", key=f"e_email_{id_sel}")

            col1, col2, col3 = st.columns(3)
            with col1:
                fecha_primera_consulta = st.date_input("Primera consulta *", value=fpc,
                    min_value=date(2000, 1, 1), max_value=date(2030, 12, 31), key=f"e_fpc_{id_sel}")
            with col2:
                modalidad = st.selectbox("Modalidad *", ["presencial", "online"],
                    index=0 if p[8] == "presencial" else 1, key=f"e_mod_{id_sel}")
            with col3:
                tipo = st.selectbox("Tipo *", ["particular", "obra social"],
                    index=0 if p[9] == "particular" else 1, key=f"e_tipo_{id_sel}")

            es_os = tipo == "obra social"
            nro_afiliado_val = p[15] if len(p) > 15 and p[15] else ""

            col1, col2 = st.columns(2)
            with col1:
                obra_social = st.text_input("Obra social", value=p[10] or "",
                    disabled=not es_os, key=f"e_os_{id_sel}")
            with col2:
                nro_afiliado = st.text_input("Nro de afiliado", value=nro_afiliado_val,
                    disabled=not es_os, key=f"e_nro_{id_sel}")

            patologia = st.text_input("Patología / Motivo", value=p[7] or "", key=f"e_pat_{id_sel}")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                moneda = st.selectbox("Moneda *", ["ARS", "USD", "EUR"],
                    index=["ARS","USD","EUR"].index(p[11]) if p[11] in ["ARS","USD","EUR"] else 0,
                    key=f"e_mon_{id_sel}")
            with col2:
                precio_sesion = st.number_input("Precio por sesión *",
                    min_value=0.0, value=float(p[12] or 0), key=f"e_precio_{id_sel}")
            with col3:
                pais_residencia = st.text_input("País de residencia *", value=p[13] or "",
                    key=f"e_pais_{id_sel}")
            with col4:
                estado = st.selectbox("Estado", ["activo", "inactivo"],
                    index=0 if p[14] == "activo" else 1, key=f"e_estado_{id_sel}")

            if st.button("Guardar cambios", key=f"btn_editar_{id_sel}"):
                errores = []
                if not nombre: errores.append("Nombre es obligatorio.")
                if not apellido: errores.append("Apellido es obligatorio.")
                if not telefono: errores.append("Teléfono es obligatorio.")
                if not email: errores.append("Email es obligatorio.")
                if not pais_residencia: errores.append("País de residencia es obligatorio.")
                if precio_sesion <= 0: errores.append("El precio de sesión debe ser mayor a 0.")
                if fecha_primera_consulta <= fecha_nacimiento:
                    errores.append("La primera consulta debe ser posterior a la fecha de nacimiento.")
                if errores:
                    for e in errores:
                        st.error(e)
                else:
                    os_guardar = obra_social if es_os else None
                    nro_guardar = nro_afiliado if es_os else None
                    modificar_paciente(id_sel, nombre, apellido, str(fecha_nacimiento),
                                      telefono, email, patologia, modalidad, tipo,
                                      os_guardar, nro_guardar, moneda, precio_sesion,
                                      pais_residencia, estado)
                    st.success("Paciente actualizado correctamente.")

    with tab2:
    
        if "nuevo_tipo" not in st.session_state:
            st.session_state.nuevo_tipo = "particular"

        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre *", key="n_nombre")
        with col2:
            apellido = st.text_input("Apellido *", key="n_apellido")

        col1, col2, col3 = st.columns(3)
        with col1:
            fecha_nacimiento = st.date_input("Fecha de nacimiento *",
                value=date(1980, 1, 1), min_value=date(1900, 1, 1),
                max_value=date.today(), key="n_fn")
        with col2:
            telefono = st.text_input("Teléfono *", key="n_tel")
        with col3:
            email = st.text_input("Email *", key="n_email")

        col1, col2, col3 = st.columns(3)
        with col1:
            fecha_primera_consulta = st.date_input("Primera consulta *",
                value=date.today(), min_value=date(2000, 1, 1),
                max_value=date(2030, 12, 31), key="n_fpc")
        with col2:
            modalidad = st.selectbox("Modalidad *", ["presencial", "online"], key="n_mod")
        with col3:
            tipo = st.selectbox("Tipo *", ["particular", "obra social"], key="n_tipo")

        es_os_nuevo = st.session_state.n_tipo == "obra social"

        col1, col2 = st.columns(2)
        with col1:
            obra_social = st.text_input("Obra social", disabled=not es_os_nuevo, key="n_os")
        with col2:
            nro_afiliado = st.text_input("Nro de afiliado", disabled=not es_os_nuevo, key="n_nro")

        patologia = st.text_input("Patología / Motivo de consulta", key="n_pat")

        col1, col2, col3 = st.columns(3)
        with col1:
            moneda = st.selectbox("Moneda *", ["ARS", "USD", "EUR"], key="n_mon")
        with col2:
            precio_sesion = st.number_input("Precio por sesión *", min_value=0.0, key="n_precio")
        with col3:
            pais_residencia = st.text_input("País de residencia *", key="n_pais")

        if st.button("Guardar paciente", key="btn_nuevo"):
            errores = []
            if not nombre: errores.append("Nombre es obligatorio.")
            if not apellido: errores.append("Apellido es obligatorio.")
            if not telefono: errores.append("Teléfono es obligatorio.")
            if not email: errores.append("Email es obligatorio.")
            if not pais_residencia: errores.append("País de residencia es obligatorio.")
            if precio_sesion <= 0: errores.append("El precio de sesión debe ser mayor a 0.")
            if fecha_primera_consulta <= fecha_nacimiento:
                errores.append("La primera consulta debe ser posterior a la fecha de nacimiento.")
            if errores:
                for e in errores:
                    st.error(e)
            else:
                pacientes_existentes = listar_pacientes()
                duplicado = any(
                    p[1].lower() == nombre.lower() and p[2].lower() == apellido.lower()
                    for p in pacientes_existentes
                )
                if duplicado:
                    st.error(f"Ya existe un paciente con el nombre {nombre} {apellido}.")
                else:
                    os_guardar = obra_social if es_os_nuevo else None
                    nro_guardar = nro_afiliado if es_os_nuevo else None
                    agregar_paciente(nombre, apellido, str(fecha_nacimiento), telefono,
                                     email, str(fecha_primera_consulta), patologia,
                                     modalidad, tipo, os_guardar, nro_guardar, moneda,
                                     precio_sesion, pais_residencia)
                    st.success(f"Paciente {nombre} {apellido} guardado correctamente.")
                    st.rerun()

with tab3:
        pacientes = listar_pacientes()
        if not pacientes:
            st.info("No hay pacientes cargados.")
        else:
            opciones = {f"{p[2]}, {p[1]}": p[0] for p in pacientes}
            seleccion = st.selectbox("Seleccionar paciente", list(opciones.keys()), key="sel_hist")
            id_hist = opciones[seleccion]
            p_hist = obtener_paciente(id_hist)

            st.markdown(f"#### {p_hist[2]}, {p_hist[1]}")

            sesiones = listar_sesiones_paciente(id_hist)
            sesiones_ord = sorted(sesiones, key=lambda x: x[2], reverse=True)
            if sesiones_ord:
                import pandas as pd
                data = []
                for s in sesiones_ord:
                    data.append({
                        "Nro": s[2],
                        "Fecha": s[1],
                        "Modalidad": s[3],
                        "Monto paciente": f"{s[6]} {s[4]:.2f}",
                        "Monto OS": f"{s[6]} {s[5] or 0:.2f}",
                        "Cobrado": "✅" if s[7] == "si" else "❌",
                        "Forma cobro": s[8] or ""
                    })
                import pandas as pd
                st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
            else:
                st.info("Sin sesiones registradas.")
                
elif menu == "Nueva Sesión":
    st.subheader("Registrar sesión")
    pacientes = listar_pacientes()
    if not pacientes:
        st.warning("Primero cargá un paciente.")
    else:
        from sesiones import ultimo_numero_sesion, ultima_sesion_fecha

        opciones = {f"{p[2]}, {p[1]}": p[0] for p in pacientes}
        seleccion = st.selectbox("Paciente", list(opciones.keys()), key="sel_sesion")
        id_paciente = opciones[seleccion]

        # Traer datos completos del paciente
        p = obtener_paciente(id_paciente)
        nombre_completo = f"{p[2]}, {p[1]}"
        es_os = p[9] == "obra social"

        # Calcular edad
        hoy = date.today()
        try:
            fn = date.fromisoformat(p[3]) if p[3] else None
            if fn:
                edad = hoy.year - fn.year - ((hoy.month, hoy.day) < (fn.month, fn.day))
            else:
                edad = None
        except:
            edad = None

        # Calcular antigüedad
        try:
            fpc = date.fromisoformat(p[6]) if p[6] else None
            if fpc:
                anios = hoy.year - fpc.year - ((hoy.month, hoy.day) < (fpc.month, fpc.day))
                meses_ant = hoy.month - fpc.month if hoy.month >= fpc.month else 12 + hoy.month - fpc.month
                antiguedad = f"{anios} año(s) y {meses_ant} mes(es)"
            else:
                antiguedad = "Sin datos"
        except:
            antiguedad = "Sin datos"

        ultima_fecha = ultima_sesion_fecha(id_paciente)
        nro_sesion = ultimo_numero_sesion(id_paciente)

        # Panel informativo del paciente
        col1, col2, col3 = st.columns(3)
        col1.markdown(f"**Tipo:** {p[9].capitalize()}")
        if es_os:
            col1.markdown(f"**Obra social:** {p[10] or '-'}")
            col1.markdown(f"**Nro afiliado:** {p[15] or '-'}" if len(p) > 15 else "**Nro afiliado:** -")
        col2.markdown(f"**Edad:** {edad} años" if edad else "**Edad:** Sin datos")
        col2.markdown(f"**Antigüedad:** {antiguedad}")
        col3.markdown(f"**Última sesión:** {ultima_fecha or 'Sin sesiones previas'}")
        col3.markdown(f"**Próximo nro sesión:** {nro_sesion}")

                
        with st.form("form_sesion"):
            col1, col2, col3 = st.columns(3)
            with col1:
                fecha = st.date_input("Fecha de sesión", value=date.today(),
                    min_value=date(2000, 1, 1), max_value=date(2030, 12, 31))
            with col2:
                st.number_input("Número de sesión", value=nro_sesion,
                    min_value=nro_sesion, max_value=nro_sesion, disabled=True)
            with col3:
                modalidad = st.selectbox("Modalidad", ["presencial", "online"])

            col1, col2, col3 = st.columns(3)
            with col1:
                moneda = st.selectbox("Moneda", ["ARS", "USD", "EUR"],
                    index=["ARS","USD","EUR"].index(p[11]) if p[11] in ["ARS","USD","EUR"] else 0)
            with col2:
                monto_paciente = st.number_input("Monto paciente",
                    min_value=0.0, value=float(p[12] or 0))
            with col3:
                if es_os:
                    monto_obra_social = st.number_input("Monto obra social", min_value=0.0)
                else:
                    st.number_input("Monto obra social", min_value=0.0,
                        value=0.0, disabled=True)
                    monto_obra_social = 0.0

            col1, col2 = st.columns(2)
            with col1:
                cobrado = st.selectbox("¿Cobrado?", ["no", "si"])
            with col2:
                forma_cobro = st.selectbox("Forma de cobro",
                    ["efectivo", "transferencia", "tarjeta débito", "tarjeta crédito", "obra social"])

            if st.form_submit_button("Registrar sesión"):
                from sesiones import sesion_duplicada
                if sesion_duplicada(id_paciente, str(fecha)):
                    st.error(f"Ya existe una sesión para {nombre_completo} en esa fecha.")
                else:
                    agregar_sesion(id_paciente, str(fecha), nro_sesion, modalidad,
                                   monto_paciente, monto_obra_social, moneda, cobrado, forma_cobro)
                    st.session_state["msg_sesion"] = f"✅ Sesión {nro_sesion} de {nombre_completo} registrada correctamente."
                    st.rerun()

        if "msg_sesion" in st.session_state:
            st.success(st.session_state.pop("msg_sesion"))
      


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
            os_dict = {}
            for d in datos_pac:
                nombre_pac = f"{d[1]}, {d[0]}"
                os = d[2] if d[2] else None
                sesiones = d[4]
                total = d[5]
                if not os:
                    st.write(f"&nbsp;&nbsp;&nbsp;{nombre_pac} | {sesiones} ses. | {moneda} {total:,.2f}")
                else:
                    if os not in os_dict:
                        os_dict[os] = {"total": 0, "pacientes": []}
                    os_dict[os]["total"] += total
                    os_dict[os]["pacientes"].append((nombre_pac, sesiones, total))
            for os_nombre, os_data in os_dict.items():
                st.markdown(f"**Obra Social: {os_nombre}** — subtotal {moneda} {os_data['total']:,.2f}")
                for pac, ses, tot in os_data["pacientes"]:
                    st.write(f"&nbsp;&nbsp;&nbsp;{pac} | {ses} ses. | {moneda} {tot:,.2f}")
            st.markdown("---")
