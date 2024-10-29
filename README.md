# API de Transcrição e Busca de Códigos SAP

Este repositório contém uma aplicação backend desenvolvida com FastAPI para transcrever áudios, resumir textos e buscar códigos SAP de ferramentas e equipamentos. A aplicação utiliza a API OpenAI para realizar a transcrição de áudio e o resumo de textos.

## Estrutura do Projeto

O projeto é composto pelos seguintes arquivos principais:

- app.py: O arquivo principal da API FastAPI.
- ferramentas.py: Contém um dicionário com materiais e equipamentos e seus respectivos códigos SAP.
- LLMfunctionalitys.py: Implementa funcionalidades relacionadas à transcrição de áudio e resumo de texto usando a API OpenAI.
    - transcrever_audio(audio): Transcreve o áudio enviado usando o modelo Whisper da OpenAI.
    - buscar_codigo_sap(nome_ferramenta, caminho_arquivo="Colinha de Códigos SAP.xlsx")`: A ideia é percorrer cada uma das ferramentas contidas no dicionário e verificar se ela foi dita no áudio ou não. Isso garante que todas as ferramentas serão listadas, mesmo se forem ditas mais vezes.

# Pré-Requisitos

Certifique-se de ter o Python 3.7 ou superior instalado em sua máquina. Além disso, instale as dependências necessárias:

bash
pip install fastapi uvicorn requests pandas openai


## Run backend

- python -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- uvicorn app:app --reload --port 5000

## Run frontend

- npm install
- npm start

## Créditos

Projeto feito durante um Hackathon por: Bruna Bariccatti, Eduarda Neumann e Juliana Pirolla. (Aprimorado posteriormente)
