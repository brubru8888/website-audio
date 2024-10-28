import requests
import pandas as pd
import openai

api_key = ""

class LLMFunc:

    def transcrever_audio(audio):
        url = "https://api.openai.com/v1/audio/transcriptions"
        headers = {"Authorization": f"Bearer {api_key}", 
                   'Content-Type': 'application/json'}
        data = {"model": "whisper-1"}

        files = {
            'file': audio,
            'model': 'whisper-1'
        }

        response = requests.post(url, headers=headers, files=files, data=data)
        print(response.status_code)
        
        if response.status_code == 200:
            texto_transcrito = response.json()["text"]
            return texto_transcrito
        elif response.status_code == 429:
            print("Erro 429: Limite de solicitações atingido. Tente novamente mais tarde.")
            return None
        else:
            print(f"Erro na transcrição: {response.status_code}")
            return None

    def resumir_texto(texto):
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "Você é um assistente que resume textos."},
                {"role": "user", "content": f"Resuma o seguinte texto:\n\n{texto}"}
            ],
            "temperature": 0.5
        }

        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            resumo = response.json()["choices"][0]["message"]["content"].strip()
            return resumo
        else:
            print(f"Erro ao resumir o texto: {response.status_code}")
            return None

    def buscar_codigo_sap(nome_ferramenta, caminho_arquivo="Colinha de Códigos SAP.xlsx"):
        df = pd.read_excel(caminho_arquivo)
        ferramenta = df[df["Descrição do Material/Equipamento"].str.lower() == nome_ferramenta.lower()]

        if not ferramenta.empty:
            codigo_sap = ferramenta.iloc[0]["Código SAP"]
            return f"Código SAP da ferramenta '{nome_ferramenta}': {codigo_sap}"
        else:
            return f"Ferramenta '{nome_ferramenta}' não encontrada no arquivo."

    def transcrever_e_buscar(audio, caminho_arquivo_excel="Colinha de Códigos SAP.xlsx"):
        nome_ferramenta = LLMFunc.transcrever_audio(audio)
        if nome_ferramenta:
            print(f"Ferramenta transcrita: {nome_ferramenta}")
            resultado = LLMFunc.buscar_codigo_sap(nome_ferramenta, caminho_arquivo_excel)
            print(resultado)
        else:
            print("Erro ao transcrever o áudio.")