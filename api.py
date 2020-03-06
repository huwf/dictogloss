import io
import os
import google.api_core.exceptions
# from google.cloud import speech
from google.cloud import speech_v1 as speech

# Moved to models.Transcript
def get_transcript(filepath, encoding=speech.enums.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
                   sample_rate=44100, language_code='sv-SE', automatic_punctuation=False):

    client = speech.SpeechClient()

    with io.open(filepath, 'rb') as f:
        content = f.read()

    audio = speech.types.RecognitionAudio(content=content)

    config = speech.types.RecognitionConfig(encoding=encoding, sample_rate_hertz=sample_rate,
                                            language_code=language_code, enable_automatic_punctuation=automatic_punctuation)

    # config = {
    #     'enable_automatic_punctuation': automatic_punctuation, 'encoding': encoding, 'sample_rate_hertz': sample_rate
    # }
    # with io.open(filepath, 'rb') as f:
        # audio = {'content': f.read()}
    result = client.recognize(config, audio)

    transcript = ''
    confidence = 0
    for r in result.results:
        confidence = r.alternatives[0].confidence
        transcript += r.alternatives[0].transcript
        # print(u'Transcript: {}\nConfidence: {}'.format(r.alternatives[0].transcript, r.alternatives[0].confidence))
    return transcript, confidence


if __name__ == '__main__':
    print(get_transcript('static/mp3/12/30_6760912.0002.mp3', automatic_punctuation=True))
    # sample_recognize('static/mp3/12/30_6760912.0000.mp3')