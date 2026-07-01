import streamlit as st
from supabase import create_client

st.title("Prueba Supabase")

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

if st.button("Probar INSERT"):

    try:
        r = supabase.table("paciente").insert({
            "nombre": "Juan",
            "apellido": "Prueba"
        }).execute()

        st.success("INSERT OK")
        st.write(r.data)

    except Exception as e:
        st.exception(e)
