import streamlit as st
import pandas as pd
import json
from datetime import datetime

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="BioTech SaaS 4.0", layout="wide")

# 2. BANCO DE DADOS EM MEMÓRIA (PERSISTENTE NA SESSÃO)
if 'estoque' not in st.session_state:
    st.session_state.estoque = pd.DataFrame([
        {"RFID": "EPC-101", "Produto": "Amoxicilina 500mg", "Status": "Disponível"},
        {"RFID": "EPC-102", "Produto": "Insulina Glargina", "Status": "Disponível"},
        {"RFID": "EPC-103", "Produto": "Reagente PCR-X", "Status": "Disponível"}
    ])

if 'logs' not in st.session_state:
    st.session_state.logs = []

# 3. INTERFACE EM COLUNAS
st.title("🛡️ BioTech SaaS: Hub de Saúde Interoperável")
col_medico, col_farmacia = st.columns([1, 2])

# --- COLUNA 1: O MÉDICO (EMISSOR) ---
with col_medico:
    st.header("👨‍⚕️ Prontuário Médico")
    with st.container(border=True):
        paciente = st.text_input("Nome do Paciente", "João da Silva")
        med_prescrito = st.selectbox("Prescrever Medicamento", ["Amoxicilina 500mg", "Insulina Glargina", "Reagente PCR-X"])
        
        if st.button("🚀 Enviar Prescrição (Padrão FHIR)"):
            # Gerando o JSON HL7 FHIR
            fhir_data = {
                "resourceType": "MedicationRequest",
                "subject": {"display": paciente},
                "medicationReference": {"display": med_prescrito}
            }
            
            # LÓGICA DE INTERCEPTAÇÃO (O que a API faria)
            idx = st.session_state.estoque[
                (st.session_state.estoque['Produto'] == med_prescrito) & 
                (st.session_state.estoque['Status'] == 'Disponível')
            ].index
            
            if not idx.empty:
                st.session_state.estoque.at[idx[0], 'Status'] = f"RESERVADO: {paciente}"
                st.session_state.logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] {med_prescrito} reservado para {paciente}")
                st.success("Enviado com Sucesso!")
            else:
                st.error("Erro: Produto sem estoque!")

# --- COLUNA 2: A FARMÁCIA/LAB (RECEPTOR) ---
with col_farmacia:
    st.header("📦 Dashboard da Unidade")
    
    tab1, tab2 = st.tabs(["Estoque RFID", "Logs de Integração"])
    
    with tab1:
        st.write("Monitoramento de Prateleiras em Tempo Real")
        st.table(st.session_state.estoque)
        
    with tab2:
        for log in reversed(st.session_state.logs):
            st.info(log)

# Rodapé Técnico
st.divider()
st.caption("Protótipo SaaS Indústria 4.0 - Interoperabilidade HL7 FHIR + RFID")
