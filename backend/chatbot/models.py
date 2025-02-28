from django.db import models
from django.core.files.storage import default_storage
import os


class Assistant(models.Model):
    name = models.CharField(max_length=255)
    model_type = models.CharField(max_length=100, default="gpt-3.5-turbo")
    api_key = models.CharField(max_length=500)
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class UploadedFile(models.Model):
    assistant = models.ForeignKey(Assistant, on_delete=models.CASCADE, related_name="uploaded_files")
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name


class Query(models.Model):
    assistant = models.ForeignKey(Assistant, on_delete=models.CASCADE)
    query_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query for Assistant {self.assistant.name} on {self.created_at}"


class AssistantResponse(models.Model):
    query = models.OneToOneField(Query, on_delete=models.CASCADE, related_name="response")
    response_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response for Query ID {self.query.id}"


class AssistantRunLog(models.Model):
    assistant = models.ForeignKey(Assistant, on_delete=models.CASCADE)
    thread_id = models.CharField(max_length=255)
    run_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Run {self.run_id} for Assistant {self.assistant.name}"


from django.db import models


class VoiceQuery(models.Model):
    query_text = models.TextField()
    audio_file_path = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query_text[:50]


class VoiceAssistant(models.Model):
    name = models.CharField(max_length=100)
    model_type = models.CharField(max_length=50)
    api_key = models.CharField(max_length=255)
    instructions = models.TextField()

    def __str__(self):
        return self.name


class VoiceAssistantRunLog(models.Model):
    assistant = models.ForeignKey(Assistant, on_delete=models.CASCADE)
    thread_id = models.CharField(max_length=100)
    run_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Run ID: {self.run_id} for Thread ID: {self.thread_id}"


class VoiceResponse(models.Model):
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    response_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.response_text[:50]
