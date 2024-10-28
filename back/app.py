from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from LLMFunctionalities import LLMFunc
from pydub import AudioSegment
import io
import soundfile as sf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.post('/upload')
async def upload_audio(audio: UploadFile = File(...)):
    data = await audio.read()

    LLMFunc.transcrever_e_buscar(data)

    return JSONResponse(content={'message': 'Audio uploaded successfully!'})




if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
