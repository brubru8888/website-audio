from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import requests
from ferramentas import materiais_equipamentos

app = FastAPI()

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify your frontend URL here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_API_KEY = ""
OPENAI_API_URL = "https://api.openai.com/v1/audio/transcriptions"

@app.post('/upload')
async def upload_audio(audio: UploadFile = File(...)):
    # Save the uploaded file temporarily
    file_path = f"uploads/{audio.filename}"
    
    with open(file_path, 'wb') as f:
        f.write(await audio.read())
    
    # Send the audio file to OpenAI for transcription
    transcription = await transcribe_audio(file_path)
    if transcription:
        texto_transcrito = transcription.get("text", "")
        sap = buscar_codigo_sap(texto_transcrito)
        print(sap)
        print(texto_transcrito)
    else:
        raise HTTPException(status_code=500, detail="Erro na transcrição de áudio.")
    
    # Clean up the saved audio file
    os.remove(file_path)
    
    return {"message": "Audio uploaded successfully!", "transcription": texto_transcrito, "sap_codes": sap}
    

async def transcribe_audio(file_path: str):
    print('Transcrevendo o áudio...')

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }
    
    # Prepare the files for the request
    with open(file_path, 'rb') as audio_file:
        files = {
            'file': audio_file
        }
        data = {
            'model': 'whisper-1',
            'language': 'pt',
            'temperature': 0.1,
            'prompt': "Me diga o nome das ferramentas que vou falar a seguir"
        }
        
        response = requests.post(OPENAI_API_URL, headers=headers, files=files, data=data)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
            
        return response.json()  # Return the transcription result


# Função para buscar códigos SAP no dicionário de ferramentas
def buscar_codigo_sap(texto):
    resultados = []
    
    # Itera sobre as descrições e códigos do dicionário importado
    for descricao, codigo_sap in materiais_equipamentos.items():
        if descricao.lower() in texto.lower():
            resultados.append(f"Código SAP da ferramenta '{descricao}': {codigo_sap}")

    # Verifica se algum código foi encontrado
    if not resultados:
        resultados.append("Nenhuma ferramenta encontrada no texto transcrito.")
    
    return resultados

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
