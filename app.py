import streamlit as st
import pandas as pd
from datetime import datetime
import uuid

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="BioTech SaaS 4.0", layout="wide")

# Inicialização de Banco de Dados Simulado (In-memory)
if 'estoque_rfid' not in st.session_state:
    st.session_state.estoque_rfid = pd.DataFrame([
        {"RFID": "E001", "Item": "Amoxicilina 500mg", "Status": "Disponível", "Empresa": "Farmácia Central"},
        {"RFID": "E002", "Item": "Amoxicilina 500mg", "Status": "Disponível", "Empresa": "Farmácia Central"},
        {"RFID": "E003", "Item": "Insulina Glargina", "Status": "Disponível", "Empresa": "Farmácia Central"},
    ])

if 'reservas_fhir' not in st.session_state:
    st.session_state.reservas_fhir = []

# --- LÓGICA DE NEGÓCIO ---
def processar_fhir(json_data):
    """Simula o endpoint FastAPI recebendo o MedicationRequest"""
    try:
        paciente = json_data['subject']['display']
        medicamento = json_data['medicationReference']['display']
        
        # Busca item disponível no estoque
        idx = st.session_state.estoque_rfid[
            (st.session_state.estoque_rfid['Item'] == medicamento) & 
            (st.session_state.estoque_rfid['Status'] == 'Disponível')
        ].index
        
        if not idx.empty:
            rfid_id = st.session_state.estoque_rfid.loc[idx[0], 'RFID']
            # Atualiza Status para Reservado
            st.session_state.estoque_rfid.at[idx[0], 'Status'] = f"Reservado ({paciente})"
            
            # Registra na fila de interoperabilidade
            reserva = {
                "id": str(uuid.uuid4())[:8],
                "paciente": paciente,
                "item": medicamento,
                "rfid": rfid_id,
                "hora": datetime.now().strftime("%H:%M:%S")
            }
            st.session_state.reservas_fhir.append(reserva)
            return True, rfid_id
        return False, "Sem estoque"
    except Exception as e:
        return False, str(e)

# --- INTERFACE ---
st.title("🛡️ BioTech SaaS: Hub de Interoperabilidade")

# Sidebar para simular recepção de API (Para o seu teste)
with st.sidebar:
    st.header("🔌 Gateway API HL7 FHIR")
    mock_json = st.text_area("Simular Recebimento JSON FHIR:", height=200, placeholder='{"resourceType": "MedicationRequest", ...}')
    if st.button("Simular Webhook de Entrada"):
        import json
        try:
            data = json.loads(mock_json)
            sucesso, msg = processar_fhir(data)
            if sucesso: st.success(f"Sucesso! RFID {msg} reservado.")
            else: st.error(f"Erro: {msg}")
        except: st.error("JSON Inválido")

# Dashboard Principal
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📦 Monitor de Estoque RFID (Tempo Real)")
    st.dataframe(st.session_state.estoque_rfid, use_container_width=True)

with col2:
    st.subheader("🔔 Reservas via Prontuário")
    if not st.session_state.reservas_fhir:
        st.info("Nenhuma prescrição externa pendente.")
    else:
        for res in reversed(st.session_state.reservas_fhir):
            with st.container(border=True):
                st.write(f"**Paciente:** {res['paciente']}")
                st.write(f"**Item:** {res['item']} (RFID: {res['rfid']})")
                st.caption(f"Recebido às {res['hora']} | ID: {res['id']}")
