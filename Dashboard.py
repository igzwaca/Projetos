import streamlit as st
import pandas as pd
import requests
import time
from streamlit_autorefresh import st_autorefresh
import subprocess
import sys

# Configurações do Firebase
FIREBASE_HOST = "https://urbanplanting-128db-default-rtdb.firebaseio.com/"
FIREBASE_AUTH = "ehJp3GsR9eG0bvZnmgHFvzzavFeQEaRM8zfvxlu1"

# Este URL aponta diretamente para o arquivo GLB, permitindo o carregamento correto.
MODEL_PLANT_URL = "https://raw.githubusercontent.com/igzwaca/Projetos/main/planta.glb"

# Configurações da página
st.set_page_config(layout="centered")
st.title("📊 Leitura dos Sensores")

# Histórico de dados
if "dados_historico" not in st.session_state:
    st.session_state.dados_historico = []

st_autorefresh(interval=10000, key="refresh")

area_fundo = st.empty()


# Função para pegar dados do Firebase
def dados_sensores():
    url = f"{FIREBASE_HOST}projeto/sensores.json?auth={FIREBASE_AUTH}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json() or {}
    return {}


# Pega os dados atuais
dados = dados_sensores()

# Verifica se existe o nó "sensores"; se não, pega os valores diretamente
sensores = dados.get("sensores", dados)

# Valores dos sensores
temperatura = sensores.get("temperatura", 0)
umidade = sensores.get("umidade", 0)
solo = sensores.get("umidade_terra", 0)
luminosidade = sensores.get("luminosidade", 0)

# Formata os dados
dados_formatados = {
    "Temperatura (°C)": temperatura,
    "Umidade (%)": umidade,
    "Luminosidade (lx)": luminosidade,
    "Umidade do Solo (%)": solo,
    "Tempo": time.strftime("%H:%M:%S")
}

# Atualiza histórico
st.session_state.dados_historico.append(dados_formatados)
if len(st.session_state.dados_historico) > 10:
    st.session_state.dados_historico.pop(0)

# Converte para DataFrame
df = pd.DataFrame(st.session_state.dados_historico).set_index("Tempo")

# Mostra os dados no dashboard
with area_fundo.container():
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🌡️ Temperatura", f"{temperatura} °C")
    col2.metric("💧 Umidade", f"{umidade} %")
    col3.metric("☀️ Luminosidade", f"{luminosidade} lx")
    col4.metric("🌱 Solo", f"{solo} %")

    st.line_chart(df[["Temperatura (°C)", "Umidade (%)", "Umidade do Solo (%)", "Luminosidade (lx)"]])

# Atualiza histórico (limita a 10 pontos)
st.session_state.dados_historico.append(dados_formatados)
if len(st.session_state.dados_historico) > 10:
    st.session_state.dados_historico.pop(0)

st.subheader("Dados coletados - 🔍")
st.dataframe(df.tail(10))

st.subheader("Jardim 3D 🪴🌿")

# HTML para o visualizador 3D
planta_html = f"""
<script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>

<div style="padding: 10px; border: 1px solid #ddd; border-radius: 12px;">
    <model-viewer src="{MODEL_PLANT_URL}"
                alt="Planta 3D"
                auto-rotate
                camera-controls
                shadow-intensity="1"
                exposure="1.1"
                style="width: 100%; height: 500px; background: radial-gradient(circle, #f0f0f5 0%, #e0e0e0 100%); border-radius:10px;">
        <div slot="poster" style="
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 100%; 
            background-color: #f8f8f8; 
            border-radius: 10px;
            color: #888;
            font-family: sans-serif;
            text-align: center;
        ">
            Carregando Modelo 3D...
        </div>
    </model-viewer>
</div>
"""

# Exibe o componente HTML
st.components.v1.html(planta_html, height=540)
