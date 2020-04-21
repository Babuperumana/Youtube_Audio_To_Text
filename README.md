# Youtube_Audio_To_Text
A simple python script to download audio and its subtitles from Youtube, then use google speech to text api to recognizi this audio.

# Environment
```
python 3.6
os: Linux
```

# Steps
There are only little steps to implement the function we want.

 1. Run the following line in the command line
 	```javascript
 	export GOOGLE_APPLICATION_CREDENTIALS=[path]
 	```
 	The `path` is the local file address you put `service-account-file.json` .
 
 2. Change the `uri` in the `main.py`
 	```javascript
 	uri = 'https://www.youtube.com/watch?v=LspIeUElIFA'
 	```
 	Here, you can put any Youtube video uri. 
 
 3. After running `main.py`, you will get a new dir, which contains `audio.flac`, `google_result_audio.txt`, `subtitles.vtt`. Then, you can compare the difference between the video subtitles and the text recognized by google speech to text api.

# Suggested video uri
```
https://www.youtube.com/watch?v=LspIeUElIFA
https://www.youtube.com/watch?v=bR1oIe6m-Ds
```
The duration time of video should not be too long, because it will take more time for google api to recognize the audio.
