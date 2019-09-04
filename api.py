import io
import os
import google.api_core.exceptions
from google.cloud import speech




def get_transcript(filepath, encoding=speech.enums.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
                   sample_rate=44100, language_code='sv-SE', automatic_punctuation=False):

    client = speech.SpeechClient()

    with io.open(filepath, 'rb') as f:
        content = f.read()

    audio = speech.types.RecognitionAudio(content=content)

    config = speech.types.RecognitionConfig(encoding=encoding, sample_rate_hertz=sample_rate, language_code=language_code)

    result = client.recognize(config, audio)
    transcript = ''
    confidence = 0
    for r in result.results:
        confidence = r.alternatives[0].confidence
        transcript += r.alternatives[0].transcript
        # print(u'Transcript: {}\nConfidence: {}'.format(r.alternatives[0].transcript, r.alternatives[0].confidence))
    return transcript, confidence



