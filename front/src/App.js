import "./App.css";

import React, { useState, useRef } from 'react';
import axios from 'axios';

function App() {
  const [isRecording, setIsRecording] = useState(false);
  const [audioURL, setAudioURL] = useState('');
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const [transcript, setTranscript] = useState();
  const [itens, setItens] = useState();

  const handleStartRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorderRef.current = new MediaRecorder(stream);

    mediaRecorderRef.current.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunksRef.current.push(event.data);
      }
    };

    mediaRecorderRef.current.onstop = () => {
      const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
      const audioUrl = URL.createObjectURL(audioBlob);
      setAudioURL(audioUrl);
      audioChunksRef.current = [];
      sendAudioToBackend(audioBlob);  // Call function to send audio to backend
    };

    mediaRecorderRef.current.start();
    setIsRecording(true);
  };

  const handleStopRecording = () => {
    mediaRecorderRef.current.stop();
    setIsRecording(false);
  };

  const sendAudioToBackend = async (audioBlob) => {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.wav'); // Append the Blob as a file
    
    try {
      const response = await axios.post('http://localhost:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setTranscript(response.data.transcription)
      setItens(response.data.sap_codes)
      console.log(response.data)
      console.log(response.data.transcription)
      console.log(response.data.sap_codes)
    } catch (error) {
      console.error('Error uploading audio:', error);
    }
  };

  return (
    <div className='background'>
      <h1 className="header">
        Assistente de Almoxarifado
      </h1>
      <button className='record-button' onClick={isRecording ? handleStopRecording : handleStartRecording}>
        {isRecording ? 'Parar de gravar' : 'Começar a gravar'}
      </button>
      {transcript && (
        <div className="transcribed-text">
          <h1 className="titulo">Texto identificado</h1>
          <p>{transcript}</p>
        </div>
      )}
      {itens && Object.keys(itens).length>0 && (
        <div className="equipamentos">
        <h1 className="titulo">Equipamentos identificados</h1>
        <ul className="item">
          {Object.entries(itens).map(([key, value]) => (
            <li key={key}>
              <strong>{key}:</strong> {value}
            </li>
          ))}
        </ul>
      </div>
      )}
      {itens && Object.keys(itens).length==0 && (
      <div className="equipamentos">
        <h1 className="titulo">Nenhum equipamento identificado</h1>
      </div>
      )}
    </div>
  );
}

export default App;
