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

import gspread
from google.oauth2.service_account import Credentials
import streamlit as st

def get_sheets_client():
    creds_dict = dict(st.secrets["gcp_service_account"])
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    return gspread.authorize(creds)

def importar_turnos_desde_sheets():
    try:
        client = get_sheets_client()
        sheet_id = st.secrets["sheets"]["spreadsheet_id"]
        sheet = client.open_by_key(sheet_id).sheet1
        registros = sheet.get_all_records()
        
        conn = get_connection()
        cursor = conn.cursor()
        importados = 0
        
        for r in registros:
            nombre = f"{r.get('Nombre', '')} {r.get('Apellido', '')}".strip()
            email = r.get('Email', '')
            telefono = str(r.get('Teléfono', ''))
            modalidad = r.get('Modalidad', '')
            hora = r.get('Horario preferido', '')
            mensaje = r.get('¿Querés contarme algo antes de la primera sesión?', '')
            fecha_solicitud = r.get('Marca temporal', '')
            
            if not email:
                continue
                
            # Verificar si ya fue importado
            cursor.execute("""
                SELECT COUNT(*) FROM turno_solicitado 
                WHERE email = ? AND hora = ? AND fecha_solicitud = ?
            """, (email, hora, fecha_solicitud))
            
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO turno_solicitado 
                    (nombre, email, telefono, modalidad, fecha, hora, mensaje, estado, fecha_solicitud)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 'pendiente', ?)
                """, (nombre, email, telefono, modalidad, '', hora, mensaje, fecha_solicitud))
                importados += 1
        
        conn.commit()
        conn.close()
        return importados
    except Exception as e:
        return f"Error: {e}"
