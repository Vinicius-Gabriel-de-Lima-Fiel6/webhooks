import streamlit as st
import json

st.set_page_config(page_title="Prontuário Médico Digital", page_icon="👨‍⚕️")

st.title("👨‍⚕️ Prontuário Eletrônico (Hospital X)")
st.write("Emissão de Prescrição Padrão HL7 FHIR")

with st.form("prescricao"):
    paciente = st.text_input("Nome do Paciente", "João da Silva")
    medicamento = st.selectbox("Medicamento", ["Amoxicilina 500mg", "Insulina Glargina", "Dipirona 1g"])
    dosagem = st.text_input("Posologia", "1 comprimido a cada 8 horas")
    
    # Gerador de JSON FHIR
    fhir_template = {
        "resourceType": "MedicationRequest",
        "id": "presc-2024",
        "status": "active",
        "intent": "order",
        "subject": {"display": paciente},
        "medicationReference": {"display": medicamento},
        "dispenseRequest": {"quantity": {"value": 1}}
    }
    
    enviar = st.form_submit_button("Finalizar e Enviar para Farmácia")

if enviar:
    st.success("Prescrição enviada via interoperabilidade FHIR!")
    st.code(json.dumps(fhir_template, indent=4), language="json")
    st.info("Copie o código acima e cole no 'Gateway API' do App SaaS para testar a integração.")
