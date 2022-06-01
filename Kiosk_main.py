import speech_recognition as sr 
# mp3 파일 플레이 패키지
import pygame
# 날씨 스크래핑 모듈
import API.weather_recommendation as weather_recommendation 
import requests
#tts
from gtts import gTTS
# 자체 NLP 모듈
import API.NLP as nlp

#노란 줄 뜰 경우, 콘솔 창에 pip install SpeechRecognition 입력 
#pip install pygame
#pip gtts

# 텍스트에 리스트의 아이템이 들어있는지 확인하는 메소드
def getExtractedMenubyAPI(txt, _list):
  API_URL = '이 URL 을 교체해서 실행'
  param = {'mylist':_list, 'sentence':txt}
  return requests.get(url=API_URL,params=param).json()
  
# 파일 경로를 입력받아서 음성 파일을 실행하는 메소드 
def play_mp3file(path):
  pygame.mixer.music.load(path)
  pygame.mixer.music.play()
  while pygame.mixer.music.get_busy() == True:
      continue

# 마이크로 부터 받은 음성 데이터를 전처리
def exprocess_audiodata(_speech):
    with _speech as source: 
      print("음성 인식 중!…")
      audio = r.adjust_for_ambient_noise(source) 
      audio = r.listen(source)
    return audio

count = 0
def speak_TTS(data):
    global count
    language_toSay= 'ko' #_lang = en or ko
    tts = gTTS(text=data, lang=language_toSay)
    tts.save(f'speech{count%2}.mp3')
    play_mp3file(f'speech{count%2}.mp3')
    count += 1    

#프로그램 시작
r = sr.Recognizer()
speech = sr.Microphone(device_index=1) #음성 인식 기기 (마이크) 지정.
pygame.mixer.init()

MENU = ['햄버거' , '떡볶이'] #메뉴 리스트

#날씨를 활용한 메뉴 추천
recommend = weather_recommendation.get_recommendedList() #추천메뉴를 recommend 변수로 지정

while(True): 

  #음성인식 시작
  audio = exprocess_audiodata(speech)
  try:
      # 구글 STT API 로 음성 -> 텍스트로 변환된 'txt' 변수 지정
      txt = r.recognize_google(audio, language = 'ko-KR') 
      print(f'STT 음성 인식 문장:{txt}')
      Mymenu = getExtractedMenubyAPI(txt,MENU)
      print(f"인식한 메뉴 : {Mymenu}")
      Mynums = nlp.extract_nums(txt)
      print(f"인식한 숫자: {Mynums}")
      NLPedtext = nlp.makeTextwithMenuAndNum(Mymenu,Mynums)

      if(Mymenu and len(Mymenu)==len(Mynums)): 
        # 유효한 메뉴를 최소 하나 이상 말했고, 메뉴와 갯수를 각각 전부 말한 경우
        speak_TTS(NLPedtext)
        print(f'{NLPedtext}')  

      else:
        #그 외의 경우
        ERROR_MESSAGE = "주문을 이해하지 못했어요. 메뉴이름과 개수를 각각 말해주세요."
        speak_TTS(ERROR_MESSAGE)
        print(ERROR_MESSAGE)
        #...~

  except sr.UnknownValueError:
      print("구글 STT 가 음성인식을 하지 못했습니다.")
  except sr.RequestError as e:
      print("Could not request results from Google Speech Recognition service; {0}".format(e))

