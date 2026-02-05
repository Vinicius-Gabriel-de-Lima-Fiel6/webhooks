import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import os

st.title("🕹️ Painel de Controle Digital Twin")

# 1. Carregamento Seguro (Local)
# Certifique-se de que 'meu_diagrama.png' esteja na mesma pasta do código
NOME_ARQUIVO = "meu_diagrama.png" 

@st.cache_data
def load_local_image(path):
    if os.path.exists(path):
        return Image.open(path).convert("RGB")
    else:
        # Cria uma imagem de erro caso o arquivo não exista no GitHub
        st.error(f"Arquivo {path} não encontrado no repositório!")
        return Image.new('RGB', (600, 400), color = (73, 109, 137))

bg_image = load_local_image(NOME_ARQUIVO)

# 2. Canvas para controle 2D
canvas_result = st_canvas(
    fill_color="rgba(0, 255, 0, 0.3)", # Cor de destaque
    background_image=bg_image,
    update_streamlit=True,
    height=400,
    width=600,
    drawing_mode="point", # Use 'point' para botões ou 'rect' para áreas
    key="digital_twin_canvas",
)

# 3. Lógica de controle físico
if canvas_result.json_data is not None:
    objects = canvas_result.json_data["objects"]
    if objects:
        ultimo_click = objects[-1]
        x, y = ultimo_click["left"], ultimo_click["top"]
        st.sidebar.write(f"Último comando em: X={x}, Y={y}")
        
        # Exemplo: Se clicar no centro da imagem, envia comando
        if 250 < x < 350 and 150 < y < 250:
            st.sidebar.success("✅ Comando enviado ao hardware!")
