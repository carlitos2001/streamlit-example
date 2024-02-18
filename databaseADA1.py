import ssl
import pandas as pd
import streamlit as st
from pymongo import MongoClient
import certifi

st.title("ADA 1. MongoDB")

# Función para establecer la conexión con MongoDB
def connection():
    return MongoClient("mongodb+srv://carlosorozcoucan:AKb9p75h313QTcde@prediccion2024.o0uybnz.mongodb.net/",
                       tlsCAFile=certifi.where())

# Función para obtener los datos de la base de datos
def get_data():
    conexion = connection()
    db = conexion.get_database("sample_training")
    collection = db.get_collection("companies")
    items = collection.find()
    return list(items)

# Obtener los datos
datos = get_data()

# Convertir los ObjectId a strings
for d in datos:
    d["_id"] = str(d["_id"])

# Crear el DataFrame
df = pd.DataFrame(datos)

# Limpieza adicional del DataFrame
# Convertir todas las columnas a cadenas de texto (str)
df = df.applymap(str)

# Mostrar el DataFrame limpio en Streamlit
st.subheader("DataFrame después del proceso de limpieza:")
st.dataframe(df)
