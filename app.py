import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import os
import time
import paho.mqtt.client as mqtt # Para comunicação real com hardware

# --- Configurações da Página ---
st.set_page_config(page_title="Painel de Controle Digital Twin", layout="wide")
st.title("🕹️ Painel de Controle Digital Twin 2D (HMI)")
st.markdown("Controle sistemas físicos clicando no diagrama abaixo.")

# --- 1. Carregamento Seguro da Imagem Base ---
# Certifique-se de que 'meu_diagrama.png' esteja na mesma pasta do código
NOME_ARQUIVO = "meu_diagrama.png" 

@st.cache_data
def load_local_image(path):
    """Carrega a imagem localmente ou cria uma imagem placeholder se não encontrar."""
    if os.path.exists(path):
        return Image.open(path).convert("RGB")
    else:
        st.error(f"Arquivo {path} não encontrado no repositório! Verifique se você salvou a imagem corretamente.")
        return Image.new('RGB', (600, 400), color = (73, 109, 137))

bg_image = load_local_image(NOME_ARQUIVO)

# --- 2. Configuração do MQTT (Simulação de Hardware) ---
# Esta parte conecta você ao mundo físico. Descomente para usar.
# BROKER_ADDRESS = "broker.hivemq.com" # Exemplo de broker público
# client = mqtt.Client()
# client.connect(BROKER_ADDRESS, 1883, 60)
# client.loop_start() # Inicia o loop em background

# --- 3. Interface Interativa com Canvas ---
st.sidebar.header("Status e Controle")
status_atual = st.sidebar.empty()
status_atual.info("Aguardando interação...")

canvas_result = st_canvas(
    fill_color="rgba(0, 255, 0, 0.3)", # Cor verde para destaque ao clicar
    stroke_width=2,
    background_image=bg_image,
    update_streamlit=True,
    height=400,
    width=600,
    drawing_mode="point", # Modo de clique em pontos específicos
    key="digital_twin_canvas",
)

# --- 4. Lógica de Controle e Mapeamento de Cliques ---
if canvas_result.json_data is not None:
    objects = canvas_result.json_data.get("objects", [])
    if objects:
        # Pega a posição do último clique
        ultimo_click = objects[-1]
        x, y = ultimo_click["left"], ultimo_click["top"]
        
        # Mapeamento das áreas clicáveis baseado na imagem gerada:
        if 250 < x < 350 and 150 < y < 250: # Área central do motor principal
            status_atual.success(f"✅ Comando: Ligar Motor Principal em X:{int(x)}, Y:{int(y)}")
            # client.publish("atuador/motor1/power", "ON") # Envia comando real via MQTT
            time.sleep(0.1) # Feedback visual rápido
        elif 50 < x < 150 and 200 < y < 300: # Área do painel esquerdo
            status_atual.warning(f"🛠️ Comando: Abrir Válvula de Entrada em X:{int(x)}, Y:{int(y)}")
            # client.publish("atuador/valvulaA/estado", "ABRIR") # Envia comando real via MQTT

