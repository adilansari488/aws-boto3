import boto3
import os
import uuid

# Initialize Transcribe client
transcribe_client = boto3.client('transcribe', region_name='eu-west-2')

def lambda_handler(event, context):
    # Example input
    # event = {
    #     "MediaFileUri": "s3://your-bucket-name/media-file.mp4"
    # }

    media_file_uri = event['MediaFileUri']
    file_extension = os.path.splitext(media_file_uri)[-1].lower()
    supported_extensions = ['.mp3', '.mp4', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.webm']
    
    # Validate file extension
    if file_extension not in supported_extensions:
        return {
            "statusCode": 400,
            "message": f"Unsupported media file type: {file_extension}. Supported types: {', '.join(supported_extensions)}"
        }
    
    # Generate a unique transcription job name
    job_name = f"transcribe-job-{uuid.uuid4().hex[:8]}"
    
    # Create transcription job
    try:
        response = transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': media_file_uri},
            MediaFormat=file_extension.strip('.'),
            IdentifyMultipleLanguages=True  # Automatically detect language
        )
        return {
            "statusCode": 200,
            "message": "Transcription job started successfully",
            "JobName": response['TranscriptionJob']['TranscriptionJobName'],
            "JobStatus": response['TranscriptionJob']['TranscriptionJobStatus']
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "message": "Failed to start transcription job",
            "error": str(e)
        }
