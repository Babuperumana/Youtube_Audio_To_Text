from __future__ import unicode_literals
import youtube_dl
import os
from word_time import sample_long_running_recognize
from google.cloud import storage

def download_audio(video_uri, directory_name, current_file):
    origin = set(os.listdir(current_file))
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'flac',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_uri])
    final = set(os.listdir(current_file))
    tem_name = ''.join(final.difference(origin))
    os.rename(tem_name, directory_name + 'audio'+ '.flac')
    print('Download audio finished......')
    return

def download_subtitles(video_uri, directory_name, current_file, subtitle_status=1):
    origin = set(os.listdir(current_file))
    if subtitle_status:
        ydl_opts = {
            # Write subtitle file
            'writesubtitles': True,
            'skip_download' : True,
        }
    else:
        ydl_opts = {
            # Write automatically generated subtitle file (YouTube only)
            'writeautomaticsub': True,
            'skip_download' : True,
        }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_uri])
    final = set(os.listdir(current_file))
    tem_name = ''.join(final.difference(origin))
    if tem_name != '':
        os.rename(tem_name, directory_name + 'subtitles'+ '.vtt')
        print('Download subtitles finished ......')
    else:
        download_subtitles(video_uri, directory_name, current_file, subtitle_status=0)
    return

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )


if __name__=="__main__":
    uri = 'https://www.youtube.com/watch?v=LspIeUElIFA'
    # uri = 'http://www.youtube.com/watch?v=BaW_jenozKc'
    dir_name = uri.split('watch?v=')[1] + '/' 
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    cur_file = '/home/yanzhiyu/YanSpeech2Text/'
    download_audio(uri, dir_name, cur_file)
    download_subtitles(uri, dir_name, cur_file)
    bucket_name = 'speech_yzy'
    upload_blob(bucket_name, cur_file + dir_name + 'audio.flac', 'audio.flac')
    sample_long_running_recognize('gs://' + bucket_name + '/audio.flac', cur_file + dir_name)