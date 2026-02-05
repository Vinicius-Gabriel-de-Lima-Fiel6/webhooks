import streamlit as st
# Importa o pacote corrigido para compatibilidade com o Streamlit Cloud
from streamlit_drawable_canvas_fix import st_canvas 
from PIL import Image
import os
import time
# import paho.mqtt.client as mqtt # Descomente se for usar hardware real

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
        # Cria uma imagem placeholder para evitar o erro PIL.UnidentifiedImageError
        return Image.new('RGB', (600, 400), color = (73, 109, 137))

bg_image = load_local_image(NOME_ARQUIVO)

# --- 2. Configuração do MQTT (Simulação de Hardware) ---
# Descomente e configure seu broker para conectar ao hardware físico
# BROKER_ADDRESS = "broker.hivemq.com" # Exemplo de broker público
# client = mqtt.Client()
# client.connect(BROKER_ADDRESS, 1883, 60)
# client.loop_start() # Inicia o loop em background

# --- 3. Interface Interativa com Canvas ---
st.sidebar.header("Status e Controle")
status_atual = st.sidebar.empty()
status_atual.info("Aguardando interação...")

# O Canvas permite que você clique na imagem e capture as coordenadas
canvas_result = st_canvas(
    fill_color="rgba(0, 255, 0, 0.3)", # Cor verde para destaque ao clicar
    stroke_width=2,
    background_image=bg_image,
    update_streamlit=True,
    height=400,
    width=600,
    drawing_mode="point", # Modo de clique em pontos específicos (botões)
    key="digital_twin_canvas",
)

# --- 4. Lógica de Controle e Mapeamento de Cliques ---
if canvas_result.json_data is not None:
    objects = canvas_result.json_data.get("objects", [])
    if objects:
        # Pega a posição do último clique (o mais recente na lista)
        ultimo_click = objects[-1]
        x, y = ultimo_click["left"], ultimo_click["top"]
        
        # Mapeamento das áreas clicáveis baseado na imagem 'meu_diagrama.png':
        if 250 < x < 350 and 150 < y < 250: # Área central do motor principal
            status_atual.success(f"✅ Comando: Ligar Motor Principal em X:{int(x)}, Y:{int(y)}")
            # Descomente para enviar o comando real:
            # client.publish("atuador/motor1/power", "ON") 
            time.sleep(0.1) # Pequena pausa para feedback visual
        elif 50 < x < 150 and 200 < y < 300: # Área do painel esquerdo/válvula
            status_atual.warning(f"🛠️ Comando: Abrir Válvula de Entrada em X:{int(x)}, Y:{int(y)}")
            # Descomente para enviar o comando real:
            # client.publish("atuador/valvulaA/estado", "ABRIR")

