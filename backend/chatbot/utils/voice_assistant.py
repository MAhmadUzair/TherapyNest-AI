import os
import openai
import speech_recognition as sr
from gtts import gTTS
from django.conf import settings


temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

custom_prompt = """
You are a virtual doctor assistant named Dr. Assist... (truncated for brevity)
"""

def text_to_speech(text):
    tts = gTTS(text)
    audio_path = os.path.join(temp_dir, "temp_response.mp3")
    tts.save(audio_path)
    return audio_path

def record_audio():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Listening for input...")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    audio_path = os.path.join(temp_dir, "live_audio.wav")
    with open(audio_path, "wb") as f:
        f.write(audio.get_wav_data())

    return audio_path

def handle_voice_input_audio(audio_file):
    received_audio_path = os.path.join(temp_dir, 'received_audio.wav')
    with open(received_audio_path, 'wb') as f:
        for chunk in audio_file.chunks():
            f.write(chunk)

    with open(received_audio_path, "rb") as audio_file_obj:
        transcription = openai.Audio.transcribe("whisper-1", audio_file_obj)

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{
            "role": "system", "content": custom_prompt
        }, {
            "role": "user", "content": transcription['text']
        }]
    ).choices[0].message['content']

    audio_path = text_to_speech(response)
    return audio_path
