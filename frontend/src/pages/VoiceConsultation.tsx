import React, { useState } from 'react';
import { Mic, MicOff, Play, Square } from 'lucide-react';

const VoiceConsultation = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [recordings, setRecordings] = useState([
    { id: 1, duration: '2:30', status: 'AI Response Ready' }
  ]);

  const toggleRecording = () => {
    setIsRecording(!isRecording);
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="bg-white rounded-lg shadow-lg overflow-hidden">
        <div className="p-4 bg-indigo-600">
          <h1 className="text-xl font-semibold text-white">Voice Therapy Session</h1>
        </div>

        <div className="p-6 space-y-8">
          {/* Recording Interface */}
          <div className="text-center">
            <div className="mb-4">
              <button
                onClick={toggleRecording}
                className={`w-20 h-20 rounded-full flex items-center justify-center ${
                  isRecording
                    ? 'bg-red-500 hover:bg-red-600'
                    : 'bg-indigo-600 hover:bg-indigo-700'
                }`}
              >
                {isRecording ? (
                  <MicOff className="w-8 h-8 text-white" />
                ) : (
                  <Mic className="w-8 h-8 text-white" />
                )}
              </button>
            </div>
            <p className="text-gray-600">
              {isRecording ? 'Recording in progress...' : 'Click to start recording'}
            </p>
          </div>

          {/* Recordings List */}
          <div>
            <h2 className="text-xl font-semibold mb-4">Your Recordings</h2>
            <div className="space-y-4">
              {recordings.map((recording) => (
                <div
                  key={recording.id}
                  className="bg-gray-50 p-4 rounded-lg flex items-center justify-between"
                >
                  <div>
                    <p className="font-medium">Recording {recording.id}</p>
                    <p className="text-sm text-gray-600">Duration: {recording.duration}</p>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="text-sm text-indigo-600">{recording.status}</span>
                    <button className="p-2 text-gray-600 hover:text-indigo-600">
                      <Play className="w-5 h-5" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Guidelines */}
          <div className="bg-indigo-50 p-6 rounded-lg">
            <h3 className="font-semibold mb-2">Voice Session Guidelines</h3>
            <ul className="list-disc list-inside space-y-2 text-gray-600">
              <li>Find a quiet, private space for your session</li>
              <li>Speak clearly and at a normal pace</li>
              <li>Each recording can be up to 5 minutes long</li>
              <li>You'll receive an AI response shortly after your recording</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VoiceConsultation;
