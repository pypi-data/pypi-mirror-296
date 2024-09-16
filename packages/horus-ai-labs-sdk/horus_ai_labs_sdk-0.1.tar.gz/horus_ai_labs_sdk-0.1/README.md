from horus_labs.client import HorusLabsSDKfrom horus_labs.client import HorusLabsClient

# Horus AI Labs SDK

[![PyPI version](https://badge.fury.io/py/my-sdk.svg)](https://badge.fury.io/py/horus-ai-labs-sdk)

This is a Python SDK for interacting with the video processing service. With this SDK, you can upload videos, check the indexing status, and prompt videos to get relevant clip URLs based on prompts.

## Features

- **Upload Videos**: Upload a video to the backend for processing. The API accepts a local video file reference. 
- **Check Indexing Status**: Check the progress of video indexing.
- **Prompt Video**: Get relevant video clips by providing search prompts.

## Installation

To install the SDK, run:

```bash
pip install horus-ai-labs-sdk
```

## Usage
### 1. Upload a Video
   This method uploads a video to the backend. You will receive a request_id and an S3 URL for uploading the video.

```python
from my_sdk import VideoSDK

api_key = "your-api-key"
horus_labs_sdk = HorusLabsSDK(api_key=api_key)

# Upload video: Response contains a request_id which can 
# be used to reference the video in subsequent requests.
request_id = horus_labs_sdk.upload_video(file_path="path/to/video.mp4")
```

### 2. Check Index Status
   Use this method to check the progress of indexing the uploaded video.

```python
# Check index status using request_id
status = horus_labs_sdk.check_status(request_id)
print(f"Indexing status: {status}")
```

### 3. Prompt Video for Clip URLs
   Once the video is indexed, you can prompt the video with a query to retrieve relevant clip URLs.

```python
# Prompt the video with a search term
prompt = "search term"
clip_urls = horus_labs_sdk.prompt_video(request_id, prompt)

for clip in clip_urls:
    print(f"Clip URL: {clip}")
```

## API Methods
### 1. upload_video(file_path: str) -> dict
   `file_path`: Path to the video file to upload.

   `Returns`: A request_id which will be used to reference the video in subsequent requests.

### 2. check_status(request_id: str) -> str
   `request_id`: The ID received when uploading the video.

   `Returns`: The current status of the video indexing process. Possible values: NOT_STARTED, IN_PROGRESS, COMPLETED, ERROR.

### 3. prompt_video(request_id: str, prompt: str) -> list
   `request_id`: The ID of the video that has been indexed.

   `prompt`: The search prompt to match relevant video clips.

   `Returns`: A list of URLs to the matching video clips.
   Authentication
   This SDK requires an API key for authentication. You can pass the API key when initializing the VideoSDK class:

```python
horus_labs_sdk = HorusLabsClient(api_key="your-api-key")
```

Requirements
- Python 3.6+
- `requests`

## Contributing
Feel free to open issues or pull requests for any improvements.

## API Key
In order to request an `api_key`, please contact [horusailabs@gmail.com](mailto:horusailabs@gmail.com) or visit [horusailabs.com](https://horusailabs.com).
