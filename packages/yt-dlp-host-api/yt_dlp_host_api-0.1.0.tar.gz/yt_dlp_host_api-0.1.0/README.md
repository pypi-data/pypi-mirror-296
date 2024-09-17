# [yt-dlp-host](https://github.com/Vasysik/yt-dlp-host) API Client

This is a Python library for interacting with the [yt-dlp-host](https://github.com/Vasysik/yt-dlp-host) API.

## Installation

You can install the library using pip:

```
pip install yt-dlp-host-api
```

## Usage

Here's a basic example of how to use the library:

```python
import yt_dlp_host_api

# Initialize the API client
api = yt_dlp_host_api.api('http://your-api-url.com')
client = api.get_client('YOUR_API_KEY')

# Download a video
client.get_video(url='https://youtu.be/1FPdtR_5KFo').save_file("test_video.mp4")
print("Video saved to test_video.mp4")

# Download a audio
client.get_audio(url='https://youtu.be/1FPdtR_5KFo').save_file("test_audio.mp3")
print("Audio saved to test_audio.mp3")

# Get info
info_json = client.get_info(url='https://youtu.be/1FPdtR_5KFo').get_json(['qualities', 'title'])
print("Video info:", info_json)

# Admin operations (requires admin API key)
new_key = client.create_key("user_key", ["get_video", "get_audio", "get_info"])
keys = client.get_keys()
key = client.get_key("user_key")
client.delete_key("user_key")
```

## Features

- Download YouTube videos
- Retrieve video information
- Checking client permissions
- Admin operations:
  - Create new API keys
  - List existing API keys
  - Get API key by key name
  - Delete API keys

## API Reference

### Client

- `client.get_video(url, quality='best')`: Simple way to get the result of get_video
- `client.get_audio(url)`: Simple way to get the result of get_audio
- `client.get_live_video(url, duration, start=0, quality='best')`: Simple way to get the result of get_live_video
- `client.get_live_audio(url, duration, start=0)`: Simple way to get the result of get_live_audio
- `client.get_info(url)`: Simple way to get the result of get_info
- `client.send_task.get_video(url, quality='best')`: Initiates a get_video task
- `client.send_task.get_audio(url)`: Initiates a get_audio task
- `client.send_task.get_live_video(url, duration, start=0, quality='best')`: Initiates a get_video task
- `client.send_task.get_live_audio(url, duration, start=0)`: Initiates a get_audio task
- `client.send_task.get_info(url)`: Initiates a get_info task
- `client.check_permissions(permissions)`: Checks for all permissions in the list

### Task

- `task.get_status()`: Get the current status of a task
- `task.get_result()`: Wait for and return the result of a task

### TaskResult

- `result.get_file()`: Get the file
- `result.get_file_url()`: Get the URL of the downloaded file
- `result.save_file(path)`: Save the downloaded file to the specified path
- `result.get_json(fields=None)`: Get the JSON data for info tasks (optionally filtered by fields)

### Admin

- `client.create_key(name, permissions)`: Create a new API key
- `client.get_keys()`: List all existing API keys
- `client.get_key(name)`: Get API key by key name
- `client.delete_key(name)`: Delete an API key

## Error Handling

The library uses exceptions to handle errors. Catch `yt_dlp_host_api.exceptions.APIError` to handle API-related errors.

## Contributing

Contributions to yt-dlp-host-api are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue on the GitHub repository. Pull requests are also encouraged.
