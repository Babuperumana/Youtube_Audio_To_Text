from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
import io

def sample_long_running_recognize(storage_path, save_path):
    """
    Print start and end time of each word spoken in audio file from Cloud Storage

    Args:
      storage_path can be URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
                        or local file path
    """

    client = speech_v1.SpeechClient()

    # storage_uri = 'gs://cloud-samples-data/speech/brooklyn_bridge.flac'

    # When enabled, the first result returned by the API will include a list
    # of words and the start and end time offsets (timestamps) for those words.
    enable_word_time_offsets = True

    # The language of the supplied audio
    language_code = "en-US"
    encoding = enums.RecognitionConfig.AudioEncoding.FLAC
    config = {
        "enable_word_time_offsets": enable_word_time_offsets,
        "language_code": language_code,
        "audio_channel_count": 2,
        # "sample_rate_hertz": 8000,
        "encoding": encoding,
    }
    if 'gs://' == storage_path[:5]:
        audio = {"uri": storage_path}
    else:
        with io.open(storage_path, "rb") as f:
            content = f.read()
        audio = {"content": content}

    operation = client.long_running_recognize(config, audio)
    

    print(u"Waiting for operation to complete...")
    response = operation.result()

    name = storage_path.split('/')[-1].split('.')[0]
    with open(save_path + 'google_result_' + name + '.txt', 'w') as f:
        for result in response.results:
            # First alternative is the most probable result
            alternative = result.alternatives[0]
            f.write(u"Transcript: {}".format(alternative.transcript) + '\n')
            # Write the start and end time of each word
            for word in alternative.words:
                f.write(u"Word: {}".format(word.word) + '\n')
                f.write(u"Start time: {} seconds {} nanos".format(
                        word.start_time.seconds, word.start_time.nanos
                    ) + '\n')
                f.write(u"End time: {} seconds {} nanos".format(
                        word.end_time.seconds, word.end_time.nanos
                    ) + '\n')
        f.close()
    print('analysis finished')

if __name__=="__main__":
    # sample_long_running_recognize('gs://speech_yzy/commercial_mono.wav')
    sample_long_running_recognize('/home/yanzhiyu/YanSpeech2Text/IMhMuVvXCVw/audio.flac', '')
    # export GOOGLE_APPLICATION_CREDENTIALS="/home/yanzhiyu/YanSpeech2Text/service-account-file.json"