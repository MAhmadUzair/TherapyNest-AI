import os
import openai
import logging
from django.core.files.storage import default_storage
from dotenv import load_dotenv
from ..models import Assistant, UploadedFile, Query, AssistantRunLog, AssistantResponse
import pdfplumber

load_dotenv()

custom_prompt = """
You are a virtual doctor assistant named Dr. Assist, created to provide helpful, accurate, and empathetic medical advice to users. 
...
"""

def extract_text_from_pdf(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n" if page.extract_text() else ""
            return text
    except Exception as e:
        raise Exception(f"Error reading PDF file: {str(e)}")

def process_financial_assistant_request(request):
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("API key not found in environment variables")

        client = openai.OpenAI(api_key=api_key)

        assistant = client.beta.assistants.create(
            name="Dr. Assist Assistant",
            instructions=custom_prompt,
            model="gpt-3.5-turbo",
            tools=[{"type": "file_search"}],
        )

        vector_store = client.beta.vector_stores.create(name="Financial Statements")

        uploaded_file = request.FILES.get("file")
        if not uploaded_file:
            raise ValueError("No file provided")

        file_path = default_storage.save(f"uploads/{uploaded_file.name}", uploaded_file)

        csv_text = extract_text_from_pdf(default_storage.path(file_path))
        logging.info(f"Extracted text from CSV: {csv_text[:500]}")

        file_stream = open(default_storage.path(file_path), "rb")
        file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id, files=[file_stream]
        )
        file_stream.close()

        assistant = client.beta.assistants.update(
            assistant_id=assistant.id,
            tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}}
        )

        message_file = client.files.create(
            file=open(default_storage.path(file_path), "rb"), purpose="assistants"
        )

        thread = client.beta.threads.create(
            messages=[{
                "role": "user",
                "content": request.data.get("query", "No query provided"),
                "attachments": [{
                    "file_id": message_file.id,
                    "tools": [{"type": "file_search"}]
                }]
            }]
        )

        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id, assistant_id=assistant.id
        )

        messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
        message_content = messages[0].content[0].text

        # Cleanup temporary file
        if os.path.exists(default_storage.path(file_path)):
            os.remove(default_storage.path(file_path))

        return message_content

    except Exception as e:
        raise Exception(f"Error processing request: {str(e)}")
