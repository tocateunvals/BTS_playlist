# app/app.py
import streamlit as st
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

# Agregar la carpeta src al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.recommender import get_recommendations, MOCK_REFERENCE_ARTISTS, MOOD_PROFILES
from src.db_utils import get_db_connection, save_user_response

# --- CONFIGURACIÓN DE PÁGINA ---
# Usamos una URL de un cuadrado rojo para el ícono de la pestaña, sin emojis.
st.set_page_config(
    page_title="BTS Playlist Recommender", 
    layout="centered",
    page_icon="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Solid_red.svg/1024px-Solid_red.svg.png"
)

# --- CSS PERSONALIZADO (Estética ARIRANG / O!RUL8,2?) ---
# Blanco, Negro, Rojo. Bordes gruesos, esquinas rectas, alto contraste.
custom_css = """
<style>
    /* Ocultar branding de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Fondo y texto global */
    .stApp {
        background-color: #ffffff;
        color: #000000;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }

    /* Tipografía */
    h1, h2, h3 {
        color: #000000;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-bottom: 4px solid #ff0000;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    h1 { font-size: 2.5rem; }
    h2 { font-size: 1.8rem; }
    h3 { font-size: 1.4rem; border-bottom: 2px solid #000000; }

    /* Tarjetas de canciones (Estilo recorte/cinta) */
    .custom-card {
        background-color: #ffffff;
        padding: 20px;
        border: 3px solid #000000;
        border-left: 10px solid #ff0000;
        margin-bottom: 15px;
        box-shadow: 5px 5px 0px #000000; /* Sombra dura para efecto collage */
    }

    /* Botones */
    .stButton>button {
        background-color: #ff0000;
        color: #ffffff;
        border: 3px solid #000000;
        border-radius: 0px; /* Esquinas rectas */
        font-weight: bold;
        text-transform: uppercase;
        font-size: 1rem;
        padding: 10px 20px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #000000;
        color: #ffffff;
        border-color: #ff0000;
    }

    /* Selectboxes y Radio buttons */
    .stSelectbox>div>div>div, .stRadio>div>div>div {
        background-color: #ffffff;
        color: #000000;
        border: 2px solid #000000;
        border-radius: 0px;
        font-weight: bold;
    }
    
    /* Barras de progreso */
    .stProgress > div > div > div > div {
        background-color: #ff0000;
        border: 1px solid #000000;
    }
    
    /* Tabs */
    button[data-baseweb="tab"] {
        background-color: #ffffff;
        color: #000000;
        border: 2px solid #000000;
        border-radius: 0px;
        font-weight: bold;
        text-transform: uppercase;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #ff0000;
        color: #ffffff;
        border-color: #000000;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- NAVEGACIÓN POR PESTAÑAS ---
tab1, tab2 = st.tabs(["Generar Playlist", "Dashboard BI"])

# ==========================================
# PESTAÑA 1: GENERADOR DE PLAYLIST
# ==========================================
with tab1:
    st.title("BTS Playlist Recommender")
    st.markdown("Genera tu playlist ideal basada en tu mood y artistas de referencia.")

    with st.form("recommendation_form"):
        st.subheader("1. Contexto")
        listens_to_bts = st.radio("¿Escuchas a BTS habitualmente?", ("no", "si"), horizontal=True)
        
        st.subheader("2. Tu Mood")
        mood_options = list(MOOD_PROFILES.keys())
        selected_mood = st.selectbox("¿Para qué mood estás buscando música?", mood_options)
        
        st.subheader("3. Artistas de Referencia")
        available_artists = list(MOCK_REFERENCE_ARTISTS.keys())
        
        col1, col2, col3 = st.columns(3)
        with col1:
            artist_1 = st.selectbox("Artista 1", ["Ninguno"] + available_artists)
        with col2:
            artist_2 = st.selectbox("Artista 2", ["Ninguno"] + available_artists)
        with col3:
            artist_3 = st.selectbox("Artista 3", ["Ninguno"] + available_artists)
        
        submitted = st.form_submit_button("Generar Playlist")

    if submitted:
        selected_artists = [a for a in [artist_1, artist_2, artist_3] if a != "Ninguno"]
        
        if not selected_mood and not selected_artists:
            st.error("Por favor, selecciona al menos un mood o un artista de referencia.")
        else:
            # 1. Guardar la respuesta en la base de datos (Neon)
            # Mapeamos "si" a "yes" para cumplir con la restricción CHECK de PostgreSQL
            db_listens_bts = "yes" if listens_to_bts == "si" else "no"
            
            try:
                save_user_response(db_listens_bts, selected_mood, artist_1, artist_2, artist_3)
            except Exception as e:
                st.error(f"Error al guardar la respuesta: {e}")

            # 2. Generar recomendaciones
            with st.spinner("Buscando las mejores coincidencias en el universo BTS..."):
                results = get_recommendations(
                    mood=selected_mood, 
                    artists=selected_artists, 
                    listens_to_bts=listens_to_bts, # El recomendador sigue usando "si"/"no" internamente
                    limit=5
                )
                
            if results:
                st.success("Playlist generada con éxito.")
                st.subheader("Tu recomendación personalizada:")
                
                for i, track in enumerate(results, 1):
                    with st.container():
                        st.markdown(f'<div class="custom-card">', unsafe_allow_html=True)
                        st.markdown(f"### {i}. {track['title']}")
                        st.markdown(f"**Artista:** {track['artist']} | **Tipo:** {track['type']}")
                        
                        similarity = max(0, 1.0 - (track['distance'] / 2.0))
                        st.progress(similarity, text=f"Match Score: {similarity:.0%}")
                        st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("No se encontraron recomendaciones con esos criterios.")

# ==========================================
# PESTAÑA 2: DASHBOARD BI
# ==========================================
with tab2:
    st.title("Dashboard de Análisis de Datos")
    st.markdown("Estadísticas descriptivas sobre las interacciones de los usuarios.")
    
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM user_responses", conn)
    conn.close()
    
    if df.empty:
        st.info("Aún no hay datos registrados. Usa la pestaña 'Generar Playlist' para crear el primer registro.")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Distribución de Conocimiento de BTS")
            freq_bts = df['listens_bts'].value_counts().reset_index()
            freq_bts.columns = ['Conoce BTS', 'Cantidad']
            st.dataframe(freq_bts, use_container_width=True)
            
            fig1, ax1 = plt.subplots(figsize=(5, 5))
            # Colores rojo y negro para el gráfico
            ax1.pie(freq_bts['Cantidad'], labels=freq_bts['Conoce BTS'].str.upper(), autopct='%1.1f%%', 
                    colors=['#ff0000', '#000000'], startangle=90, textprops={'color': 'white', 'fontweight': 'bold'})
            ax1.axis('equal')
            st.pyplot(fig1)
            
        with col2:
            st.subheader("Moods Más Solicitados")
            freq_mood = df['mood'].value_counts().reset_index()
            freq_mood.columns = ['Mood', 'Cantidad']
            st.dataframe(freq_mood, use_container_width=True)
            
            fig2, ax2 = plt.subplots(figsize=(5, 5))
            ax2.barh(freq_mood['Mood'].str.capitalize(), freq_mood['Cantidad'], color='#ff0000', edgecolor='#000000', linewidth=2)
            ax2.set_xlabel('Frecuencia', fontweight='bold')
            ax2.tick_params(colors='#000000')
            st.pyplot(fig2)
            
        st.markdown("---")
        st.subheader("Registro Completo de Respuestas")
        st.dataframe(df[['created_at', 'listens_bts', 'mood', 'artist_1', 'artist_2', 'artist_3']], use_container_width=True)