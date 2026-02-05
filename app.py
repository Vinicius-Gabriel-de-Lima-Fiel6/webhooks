import streamlit as st
import pandas as pd
import time
from datetime import datetime

# CONFIGURAÇÃO DE INTERFACE INDUSTRIAL
st.set_page_config(page_title="BioTech OS | Automação 4.0", layout="wide")

# SIMULAÇÃO DE HARDWARE (BANCO DE DADOS DA UNIDADE)
if 'dispositivos' not in st.session_state:
    st.session_state.dispositivos = {
        "Portal RFID": "Online",
        "Geladeira Inteligente": "Online",
        "Braço Robótico": "Standby"
    }

if 'estoque_interno' not in st.session_state:
    st.session_state.estoque_interno = pd.DataFrame([
        {"ID_RFID": "1001A", "Item": "Reagente Bio-X", "Local": "Gaveta 01", "Temp": "4.2°C", "Status": "Ok"},
        {"ID_RFID": "1002B", "Item": "Vacina Gripe", "Local": "Geladeira 02", "Temp": "3.8°C", "Status": "Ok"},
        {"ID_RFID": "1003C", "Item": "Insulina R", "Local": "Geladeira 02", "Temp": "4.0°C", "Status": "Ok"}
    ])

# --- HEADER INDUSTRIAL ---
st.title("📟 BioTech Operating System")
st.subheader("Automação Interna de Farmácia e Laboratório")

# --- BARRA LATERAL: CONTROLE DE HARDWARE ---
with st.sidebar:
    st.header("⚙️ Status do Hardware")
    for disp, status in st.session_state.dispositivos.items():
        st.status(f"{disp}: {status}", state="complete" if status == "Online" else "error")
    
    st.divider()
    st.header("📥 Entrada de Matéria-Prima")
    if st.button("Escanear Novo Lote (RFID)"):
        with st.spinner("Processando XML da NFe e IDs RFID..."):
            time.sleep(2)
            st.success("Lote Integrado com Sucesso!")

# --- CORPO PRINCIPAL: OPERAÇÃO AUTÔNOMA ---
col_mapa, col_alertas = st.columns([2, 1])

with col_mapa:
    st.write("### 📍 Rastreabilidade Interna em Tempo Real")
    # Aqui o diferencial: Monitoramento de temperatura POR ITEM
    st.dataframe(st.session_state.estoque_interno, use_container_width=True)
    
    if st.button("Executar Inventário Cego Autônomo"):
        st.write("🤖 Robô iniciando varredura de prateleiras...")
        bar = st.progress(0)
        for i in range(100):
            time.sleep(0.02)
            bar.progress(i + 1)
        st.success("Inventário concluído: 100% de acurácia entre Físico vs Sistema.")

with col_alertas:
    st.write("### ⚠️ Gestão de Riscos (IA)")
    with st.container(border=True):
        st.warning("Previsão: Geladeira 02 subirá para 6°C em 2h (Falha de Compressor).")
        if st.button("Acionar Manutenção Preditiva"):
            st.info("Ticket aberto com a assistência técnica.")
    
    with st.container(border=True):
        st.error("Validade Crítica: Reagente Bio-X vence em 48h.")
        st.button("Promover Desconto/Uso Prioritário")

# --- CONFORMIDADE SANITÁRIA (FOOTER) ---
st.divider()
if st.button("📄 Gerar Relatório para Vigilância Sanitária (Blockchain)"):
    st.write("Gerando histórico imutável de temperatura e movimentação...")
    st.download_button("Baixar PDF Autenticado", "Dados de auditoria...", "relatorio_conformidade.pdf")
