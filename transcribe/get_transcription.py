import boto3
import json

# Initialize Transcribe client
transcribe_client = boto3.client('transcribe', region_name='eu-west-2')

def lambda_handler(event, context):
    # Example input
    # event = {
    #     "TranscriptionJobName": "transcribe-job-abc12345"
    # }

    job_name = event.get('TranscriptionJobName')
    if not job_name:
        return {
            "statusCode": 400,
            "message": "TranscriptionJobName is required"
        }
    
    try:
        # Get transcription job details
        response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = response['TranscriptionJob']['TranscriptionJobStatus']
        
        if job_status == 'COMPLETED':
            transcript_file_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
            
            # Optionally, fetch the transcript content
            # transcript_content = fetch_transcript_content(transcript_file_uri)
            
            return {
                "statusCode": 200,
                "message": "Transcription job completed",
                "TranscriptFileUri": transcript_file_uri,
                #"TranscriptContent": transcript_content  # Optional
            }
        elif job_status == 'FAILED':
            return {
                "statusCode": 400,
                "message": f"Transcription job failed: {response['TranscriptionJob']['FailureReason']}"
            }
        else:
            return {
                "statusCode": 202,
                "message": "Transcription job is still in progress",
                "JobStatus": job_status
            }
    except Exception as e:
        return {
            "statusCode": 500,
            "message": "Failed to retrieve transcription job details",
            "error": str(e)
        }

# def fetch_transcript_content(transcript_file_uri):
#     """
#     Fetch the transcript content from the provided URI.
#     """
#     import requests
#     try:
#         response = requests.get(transcript_file_uri)
#         response.raise_for_status()  # Raise an exception for HTTP errors
#         transcript_data = response.json()
#         return transcript_data.get('results', {})
#     except Exception as e:
#         return {"error": f"Failed to fetch transcript content: {str(e)}"}
