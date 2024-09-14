from sonusai.mixture import AudioT
from sonusai.utils import ASRResult


def openai_whisper(audio: AudioT, **config) -> ASRResult:
    from typing import Optional

    from sonusai import SonusAIError
    from whisper import load_model

    model_name: Optional[str] = config.get('model', None)
    if model_name is None:
        raise SonusAIError("config must specify 'model'")

    device = config.get('device', 'cpu')

    model = load_model(model_name, device=device)

    return ASRResult(text=model.transcribe(audio, fp16=False)['text'])


"""
OpenAI Whisper results:
{
  'text': ' The birch canoe slid on the smooth planks.',
  'segments': [
    {
      'id': 0,
      'seek': 0,
      'start': 0.0,
      'end': 2.4,
      'text': ' The birch canoe slid on the smooth planks.',
      'tokens': [
        50363,
        383,
        35122,
        354,
        47434,
        27803,
        319,
        262,
        7209,
        1410,
        591,
        13,
        50483
      ],
      'temperature': 0.0,
      'avg_logprob': -0.4188103675842285,
      'compression_ratio': 0.8571428571428571,
      'no_speech_prob': 0.003438911633566022
    }
  ],
  'language': 'en'
}
"""
