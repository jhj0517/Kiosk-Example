from google.cloud import texttospeech
import json
import os
# 음성 파일 플레이 패키지
import pygame

Setting = {
    'speed':1.1,
    'voice': 'ko-KR-Wavenet-A',
    'pitch':0
}

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./API/tts_api_key.json"

client = texttospeech.TextToSpeechClient()
voice = texttospeech.VoiceSelectionParams(
    language_code="ko-KR", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    name=Setting['voice']
)
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3,
    pitch = Setting['pitch'],speaking_rate=Setting["speed"]
)

pygame.mixer.init()

def play_mp3file(path):
  pygame.mixer.music.load(path)
  pygame.mixer.music.play()
  while pygame.mixer.music.get_busy() == True:
      continue

def list_voices(language_code=None):
    client = texttospeech.TextToSpeechClient()
    response = client.list_voices(language_code=language_code)
    voices = sorted(response.voices, key=lambda voice: voice.name)

    print(f" Voices: {len(voices)} ".center(60, "-"))
    for voice in voices:
        languages = ", ".join(voice.language_codes)
        name = voice.name
        gender = texttospeech.SsmlVoiceGender(voice.ssml_gender).name
        rate = voice.natural_sample_rate_hertz
        print(f"{languages:<8} | {name:<24} | {gender:<8} | {rate:,} Hz")

"""TTS 메소드"""
count = 0
def GoogleTTS(txt):
    global count
    synthesis_input = texttospeech.SynthesisInput(text=txt)
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    open(f"speech{count%2}.mp3", "wb").write(response.audio_content)
    play_mp3file(f"speech{count%2}.mp3")
    count += 1
