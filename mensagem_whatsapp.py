import requests
import pywhatkit

import time

FIREBASE_HOST = "https://urbanplanting-128db-default-rtdb.firebaseio.com"
FIREBASE_AUTH = "ehJp3GsR9eG0bvZnmgHFvzzavFeQEaRM8zfvxlu1"

NUMEROS = ["+5592984513263"]

def pegar_dados():
    url = f"{FIREBASE_HOST}/projeto/sensores.json?auth={FIREBASE_AUTH}"
    resposta = requests.get(url)
    if resposta.status_code == 200:
        return resposta.json()
    else:
        print("❌ Erro ao  acessar o banco de dados FIREBASE", resposta.text)
        return {}

def enviar_mensagem():

    dados = pegar_dados()
    if not dados:
        print("⚠️ Nenhum dado foi encontrado")
        return

    mensagem = (
        f"🌡️ Temperatura: {dados.get('temperatura')}°C\n"
        f"💧 Umidade do ar: {dados.get('umidade')}%\n"
        f"🌱 Umidade da terra: {dados.get('umidade_terra')}%\n"
        f"☀️ Luminosidade: {dados.get('luminosidade')}"
    )

    for numero in NUMEROS:
        try:
            print(f"Agendando envio de mensagem para {numero}")
            pywhatkit.sendwhatmsg_instantly(numero, mensagem, wait_time=15, tab_close=True)
            print(f"✅ Mensagem enviada para o numero {numero}")
            time.sleep(5)
        except Exception as e:
            print(f"❌ Erro ao enviar mensagem para {numero}: {e}")

enviar_mensagem()







