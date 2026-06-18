from supabase import create_client
import streamlit as st

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase = create_client(url, key)

try:
    resultado = supabase.table("paciente").select("*").execute()
    st.sidebar.success("Supabase OK")
    st.sidebar.write("Pacientes:", len(resultado.data))
except Exception as e:
    st.sidebar.error(f"Error Supabase: {e}")
