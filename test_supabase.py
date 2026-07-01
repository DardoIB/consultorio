import streamlit as st
from supabase import create_client

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

r = supabase.table("paciente").insert({
    "nombre": "Juan",
    "apellido": "Prueba"
}).execute()

st.write(r)
