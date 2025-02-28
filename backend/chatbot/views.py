import PyPDF2
from django.core.files.uploadedfile import UploadedFile
from .utils.chat_assistant import process_financial_assistant_request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class FinancialAssistantAPI(APIView):
    def post(self, request):
        try:
            response_message = process_financial_assistant_request(request)
            return Response({"response": response_message}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



import os
import openai
import speech_recognition as sr
from gtts import gTTS
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.files.storage import default_storage
from .models import Assistant, AssistantRunLog


temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

custom_prompt = """
You are a virtual doctor assistant named Dr. Assist... (truncated for brevity)
Some Example Responses
    - When user says "what you have?" So Instead starting reply from "The uploaded file contains a variety of product information" write it as, "Here I found this information". Objective is to not let user know that you are talking from file.
- Do not tell user that you are responding from uploaded file. You just have to answer out of it.
- Do not discuss document management or file specifics, including how data is uploaded or managed.
- Never say to user "files you have uploaded?"
- Never say to user "you have any uploaded files or information"
- Avoid mentioning stock quantities or logistical details related to product availability.
- Do not talk about document uploading etc.
- You must respond immediately. Do not take much time to respond to query.
-dont talk about file in response only give to the point response.
"""

api_key = os.getenv("OPENAI_API_KEY")
client = openai.Client(api_key=api_key)


def text_to_speech(text):
    if not isinstance(text, str):
        raise ValueError(f"Expected string input but got {type(text)}: {text}")

    audio_filename = "temp_response.mp3"
    audio_path = os.path.join(settings.MEDIA_ROOT, "temp", audio_filename)

    tts = gTTS(text.strip())
    tts.save(audio_path)

    # Return the URL instead of the file path
    return settings.MEDIA_URL + f"temp/{audio_filename}"
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

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        raise Exception(f"Error reading PDF file: {str(e)}")

@csrf_exempt
def voice_input_workflow(request):
    if request.method == "POST":
        audio_file = request.FILES.get('audio_data')
        uploaded_file = request.FILES.get('file')
        if not audio_file:
            return JsonResponse({"error": "No audio data received"}, status=400)

        # Save audio file
        received_audio_path = os.path.join(temp_dir, 'received_audio.wav')
        with open(received_audio_path, 'wb') as f:
            for chunk in audio_file.chunks():
                f.write(chunk)

        # Step 1: Transcribe the audio
        try:
            with open(received_audio_path, "rb") as audio_file_obj:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file_obj
                )

            query_text = transcription.text
            if not query_text:
                return JsonResponse({"error": "No transcription result found"}, status=500)
        except Exception as e:
            return JsonResponse({"error": f"Transcription failed: {str(e)}"}, status=500)

        # Step 2: Create Assistant using OpenAI API
        try:
            assistant = client.beta.assistants.create(
                name="Voice-Based Assistant",
                instructions=custom_prompt,
                model="gpt-4-turbo-preview",
                tools=[{"type": "file_search"}]
            )
            assistant_id = assistant.id  # Ensure this retrieves the correct ID
            assistant_obj = Assistant.objects.create(
                name="Voice-Based Assistant",
                model_type="gpt-4",
                api_key=api_key,
                instructions=custom_prompt
            )
        except Exception as e:
            return JsonResponse({"error": f"Assistant creation failed: {str(e)}"}, status=500)

        # Step 3: Handle File Upload (if provided)
        if uploaded_file:
            file_path = default_storage.save(f"uploads/{uploaded_file.name}", uploaded_file)
            uploaded_file_obj = UploadedFile.objects.create(
                assistant=assistant_obj,
                file_name=uploaded_file.name,
                file_path=file_path
            )
            message_file = client.files.create(file=open(default_storage.path(file_path), "rb"), purpose="assistants")
        else:
            message_file = None

        # Step 4: Create a Thread and Send Query
        try:
            messages = [{"role": "user", "content": query_text}]
            if message_file:
                messages[0]["attachments"] = [{"file_id": message_file.id, "tools": [{"type": "file_search"}]}]
            thread = client.beta.threads.create(messages=messages)
            run = client.beta.threads.runs.create_and_poll(thread_id=str(thread.id), assistant_id=assistant_id)
            run_log_obj = AssistantRunLog.objects.create(
                assistant=assistant_obj,
                thread_id=thread.id,
                run_id=run.id
            )
            response_messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
            message_content = response_messages[0].content[0].text.value  # Extract the text correctly
        except Exception as e:
            return JsonResponse({"error": f"Thread processing failed: {str(e)}"}, status=500)

        # Step 5: Convert response to speech
        try:
            audio_path = text_to_speech(message_content)
        except Exception as e:
            return JsonResponse({"error": f"Text-to-speech conversion failed: {str(e)}"}, status=500)

        # Step 6: Cleanup uploaded file (if any)
        if uploaded_file and os.path.exists(default_storage.path(file_path)):
            os.remove(default_storage.path(file_path))

        return JsonResponse({"audio_response_path": audio_path})

    return JsonResponse({"error": "Invalid request"}, status=400)

def voice_input(request):
    return render(request, 'voice_input.html')

