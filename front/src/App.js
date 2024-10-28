import React, { useState, useRef } from 'react';
import axios from 'axios';

function AudioRecorder() {
  const [isRecording, setIsRecording] = useState(false);
  const [audioURL, setAudioURL] = useState('');
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const [transcript, setTranscript] = useState();

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
      setTranscript(response.data.transcription.text)
    } catch (error) {
      console.error('Error uploading audio:', error);
    }
  };

  return (
    <div className='background'>
      <button onClick={isRecording ? handleStopRecording : handleStartRecording}>
        {isRecording ? 'Stop Recording' : 'Start Recording'}
      </button>
      {transcript && (
        <div>
          <p>{transcript}</p>
        </div>
      )}
    </div>
  );
}

export default AudioRecorder;