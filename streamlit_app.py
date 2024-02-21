import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from pymongo import MongoClient
import certifi
import uuid

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:.
If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""
num_points = st.slider("Number of points in spiral", 1, 10000, 1100)
num_turns = st.slider("Number of turns in spiral", 1, 300, 31)

indices = np.linspace(0, 1, num_points)
theta = 2 * np.pi * num_turns * indices
radius = indices

x = radius * np.cos(theta)
y = radius * np.sin(theta)

df = pd.DataFrame({
    "x": x,
    "y": y,
    "idx": indices,
    "rand": np.random.randn(num_points),
})

st.altair_chart(alt.Chart(df, height=700, width=700)
    .mark_point(filled=True)
    .encode(
        x=alt.X("x", axis=None),
        y=alt.Y("y", axis=None),
        color=alt.Color("idx", legend=None, scale=alt.Scale()),
        size=alt.Size("rand", legend=None, scale=alt.Scale(range=[1, 150])),
    ))

# Título de la aplicación
st.title("ADA1 de MongoDB")

# Función para establecer la conexión con MongoDB
@st.cache(allow_output_mutation=True)
def connection():
    return MongoClient("mongodb+srv://" + st.secrets["DB_USERNAME"] + ":" + st.secrets["DB_PASSWORD"] + "@prediccion2024.o0uybnz.mongodb.net/", tlsCAFile=certifi.where())

# Función para obtener los datos de la base de datos
@st.cache(allow_output_mutation=True)
def get_data():
    conexion = connection()
    db = conexion.get_database("sample_training")
    collection = db.get_collection("companies")
    items = collection.find()
    return list(items)

def insert_data(new_data):
    conexion = connection()
    db = conexion.get_database("sample_training")
    collection = db.get_collection("companies")
    collection.insert_one(new_data)

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
# Seleccionar las primeras 10 filas que no tienen datos nulos y limitar a las primeras 5 columnas
df_filtered = df.dropna().iloc[:10, :5]

# Mostrar el DataFrame filtrado en Streamlit
st.subheader("Primeras 10 filas sin datos nulos y primeras 5 columnas:")
st.dataframe(df_filtered)

# Agregar un formulario para agregar nuevos datos a la base de datos
st.subheader("Agregar nuevos datos")

# Definir los campos del formulario
name = st.text_input("Nombre")
permalink = st.text_input("Permalink")
crunchbase_url = st.text_input("Crunchbase URL")
homepage_url = st.text_input("Homepage URL")

# Generar un nuevo _id aleatorio
new_id = str(uuid.uuid4())

# Verificar si el _id ya existe en la base de datos
while any(d['_id'] == new_id for d in datos):
    new_id = str(uuid.uuid4())

# Botón para agregar los datos
if st.button("Insertar"):
    new_data = {
        "_id": new_id,
        "name": name,
        "permalink": permalink,
        "crunchbase_url": crunchbase_url,
        "homepage_url": homepage_url
    }
    insert_data(new_data)
    st.success("Datos agregados correctamente")

    # Actualizar los datos después de la inserción
    datos = get_data()
    for d in datos:
        d["_id"] = str(d["_id"])

    # Agregar el nuevo dato como la primera fila
    datos.insert(0, new_data)

    df = pd.DataFrame(datos)
    df = df.applymap(str)
    st.subheader("Datos actualizados:")
    st.dataframe(df)