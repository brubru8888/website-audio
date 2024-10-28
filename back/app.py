from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify your frontend URL here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a directory to save uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post('/upload')
async def upload_audio(audio: UploadFile = File(...)):
    print("aqui")
    # Save the uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, audio.filename)
    
    with open(file_path, 'wb') as file:
        file.write(await audio.read())

    print('exec')

    return JSONResponse(content={'message': 'Audio uploaded successfully!', 'file_path': file_path})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
