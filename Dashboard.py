import streamlit as st
import pandas as pd
import requests
import time
from streamlit_autorefresh import st_autorefresh

# Configurações do Firebase
FIREBASE_HOST = "https://urbanplanting-128db-default-rtdb.firebaseio.com/"
FIREBASE_AUTH = "ehJp3GsR9eG0bvZnmgHFvzzavFeQEaRM8zfvxlu1"

# Configurações da página
st.set_page_config(layout="wide")
st.title("Dashboard - 📊 Leitura dos Sensores")

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
luminosidade = sensores.get("luminosidade", 0)
solo = sensores.get("umidade_terra", 0)

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
if len(st.session_state.dados_historico) > 20:
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

    st.line_chart(df[["Temperatura (°C)", "Umidade (%)", "Umidade do Solo (%)"]])
    st.area_chart(df[["Luminosidade (lx)"]])

