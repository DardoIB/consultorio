import streamlit as st
from supabase import create_client
from postgrest.exceptions import APIError

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

st.title("Prueba Supabase")

if st.button("Insertar"):

    try:

        r = supabase.table("paciente").insert({
            "nombre": "Juan",
            "apellido": "Prueba"
        }).execute()

        st.success("OK")
        st.write(r.data)

    except APIError as e:
        st.error("APIError")
        st.write(e.json())

    except Exception as e:
        st.error(type(e))
        st.write(str(e))
