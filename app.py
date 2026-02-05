import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import requests
from io import BytesIO

st.title("Digital Twin 2D - Cloud Version")

# URL da imagem (exemplo: diagrama de um motor ou circuito)
URL_IMAGEM = "https://upload.wikimedia.org"

@st.cache_data
def load_image(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content)).convert("RGB")

bg_image = load_image(URL_IMAGEM)

# Interface Interativa
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=2,
    background_image=bg_image,
    update_streamlit=True,
    height=400,
    width=600,
    drawing_mode="rect", # 'rect' para selecionar áreas ou 'point' para botões
    key="canvas",
)

if canvas_result.json_data is not None:
    # Lógica para ler os cliques/objetos desenhados
    objetos = canvas_result.json_data["objects"]
    if objetos:
        st.write("Interação detectada no hardware!")
        # Envie seu comando MQTT aqui
