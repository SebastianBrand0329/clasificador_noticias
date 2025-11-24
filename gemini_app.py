# --------------------------------------------------------------------------
# app.py - Aplicación simple de clasificación de noticias con Streamlit y Gemini
# --------------------------------------------------------------------------

# 1. Importar las librerías necesarias
import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# --------------------------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA Y LA API KEY
# --------------------------------------------------------------------------

# Título de la aplicación que se mostrará en la pestaña del navegador
st.set_page_config(page_title="Clasificador de Noticias", page_icon="📰")

# Título principal de la aplicación
st.title("📰 Clasificador de Noticias con Gemini")
st.caption("Pega el texto de una noticia y obtén su categoría estimada.")

# Configuración de la API Key de Google de forma segura
try:
    os.environ['GOOGLE_API_KEY'] = st.secrets['AIzaSyA4sQCZpJaV-xPvqxjQy1EUg1nQlBzOlpE']
except:
    st.info("API Key no encontrada en los secrets. Asegúrate de configurar tu archivo secrets.toml.")

# --------------------------------------------------------------------------
# COMPONENTES DE LANGCHAIN Y LÓGICA DEL MODELO
# --------------------------------------------------------------------------

# 1. Plantilla del Prompt
prompt = ChatPromptTemplate.from_template(
    """
    Eres un clasificador experto de noticias. 
    Tu tarea es leer el texto de una noticia y asignarle una categoría.

    Las categorías posibles son:
    - política
    - deportes
    - economía
    - tecnología
    - salud
    - cultura
    - internacional
    - otra

    Noticia:
    {news_text}

    Devuelve SOLO la categoría, sin explicación.
    """
)

# 2. Instancia del modelo Gemini
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.0)

# 3. Parser de salida
parser = StrOutputParser()

# 4. Crear la cadena de ejecución
chain = prompt | llm | parser

# --------------------------------------------------------------------------
# INTERFAZ DE USUARIO DE STREAMLIT
# --------------------------------------------------------------------------

# Área de texto para pegar la noticia
news_text = st.text_area(
    "Pega aquí el texto de la noticia:",
    placeholder="Escribe o pega el contenido completo de la noticia..."
)

# Botón de clasificación
if st.button("Clasificar"):
    if news_text.strip() == "":
        st.warning("Por favor ingresa el texto de una noticia.")
    else:
        with st.spinner("Clasificando noticia... 🧠"):
            try:
                # Ejecutamos el modelo
                result = chain.invoke({"news_text": news_text})

                # Mostrar resultado
                st.markdown("### 🏷️ Categoría predicha:")
                st.markdown(f"**{result}**")

            except Exception as e:
                st.error(f"Ocurrió un error al procesar la noticia: {e}")
