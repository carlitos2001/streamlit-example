import pandas as pd
import streamlit as st
from pymongo import MongoClient
import certifi

# Título de la aplicación
st.title("Prueba de conexión a MongoDB")

# Función para establecer la conexión con MongoDB
@st.experimental_singleton(suppress_st_warning=True)
def get_connection():
    return MongoClient("mongodb+srv://"+st.secrets["DB_USERNAME"]+":"+st.secrets["DB_PASSWORD"]+"@prediccion2024.o0uybnz.mongodb.net/", tlsCAFile=certifi.where())

# Función para obtener los datos de la base de datos
@st.cache(ttl=60, allow_output_mutation=True)
def get_data():
    with get_connection() as conexion:
        db = conexion.get_database("Prediccion")
        collection = db.get_collection("ejemplo 1")
        items = collection.find()
        # Convertir los resultados a una lista para evitar mutaciones directas del objeto devuelto.
        return list(items)

# Obtener los datos
datos = get_data()

# Convertir los ObjectId a strings
for d in datos:
    d["_id"] = str(d["_id"])

# Crear el DataFrame y mostrarlo en Streamlit
if datos:
    df = pd.DataFrame(datos)
    st.dataframe(df)
else:
    st.write("No se encontraron datos en la colección 'ejemplo 1'")

# Insertar nuevas tareas
st.title("Insertar Nuevas Tareas:")
Nombre = st.text_input("Nombre Tarea:")
Puntos = st.number_input("Elige una puntuación:", 0, 10)
Materia = st.text_input("Nombre de la materia:")
Fechacreacion = st.date_input("Fecha Creacion")
FechaEntrega = st.date_input("Fecha entrega")

# Manejo de inserción de datos en MongoDB
if st.button("Insertar"):
    with get_connection() as conexion:
        db = conexion.get_database("Prediccion")
        nuevaColletion = db.get_collection("inventario")
        # Insertar el nuevo registro
        nuevaColletion.insert_one({
            "Nombre": Nombre,
            "Puntos": Puntos,
            "Materia": Materia,
            "Fechacreacion": Fechacreacion,
            "FechaEntrega": FechaEntrega
        })
    st.success("¡Datos insertados correctamente!")
