#mongodb+srv://carlosorozcoucan:AKb9p75h313QTcde@prediccion2024.o0uybnz.mongodb.net/"
import ssl

import ssl
import pandas as pd
import streamlit as st
from pymongo import MongoClient
import certifi

st.title("Prueba de conexión a MongoDB")

# Función para establecer la conexión con MongoDB
def connection():
    return MongoClient("mongodb+srv://carlosorozcoucan:AKb9p75h313QTcde@prediccion2024.o0uybnz.mongodb.net/", tlsCAFile=certifi.where())

# Función para obtener los datos de la base de datos
def get_data():
    conexion = connection()
    db = conexion.get_database("Prediccion")
    collection = db.get_collection("ejemplo 1")
    items = collection.find()
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
